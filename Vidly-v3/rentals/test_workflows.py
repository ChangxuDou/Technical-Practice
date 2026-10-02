import uuid
from decimal import Decimal
from datetime import timedelta
from django.test import TestCase, override_settings, Client
from django.contrib.auth.models import User, Group
from django.core.exceptions import PermissionDenied, ValidationError
from django.utils import timezone
from movies.models import Movie, Genre
from .models import (Customer, Rental, ReturnRecord, Ledger, RewardPolicy, PolicyRevision,
                     TopUp, PointsEntry, MovieWish, WishRequest, PurchaseOrder, StockReceipt)
from .services import BusinessError, checkout, settle, adjust_balance
from .workflows import (submit_wish, create_purchase, receive_purchase, start_topup,
                        finish_topup, configure_rewards, decline_wish)

@override_settings(STORAGES={'default':{'BACKEND':'django.core.files.storage.FileSystemStorage'},'staticfiles':{'BACKEND':'django.contrib.staticfiles.storage.StaticFilesStorage'}})
class WorkflowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user=User.objects.create_user('customer',password='Test!2026Strong')
        cls.other=User.objects.create_user('other',password='Test!2026Strong')
        cls.manager=User.objects.create_user('manager',password='Test!2026Strong',is_staff=True)
        cls.cashier=User.objects.create_user('cashier',password='Test!2026Strong',is_staff=True)
        cls.superuser=User.objects.create_superuser('root','root@example.com','Test!2026Strong')
        cls.manager.groups.add(Group.objects.create(name='Manager'))
        cls.cashier.groups.add(Group.objects.create(name='Cashier'))
        cls.c=Customer.objects.create(user=cls.user,full_name='Customer',phone='1000001')
        cls.c2=Customer.objects.create(user=cls.other,full_name='Other',phone='1000002')
        cls.genre=Genre.objects.create(name='Drama')
        cls.movie=Movie.objects.create(title='Existing',release_year=2000,genre=cls.genre,barcode='1234567890',daily_rate=Decimal('3'),total_quantity=5,number_in_stock=5)

    def wish(self,user=None,title='New Story',year=2025):
        return submit_wish(user or self.user,title,year,'please')[0].wish

    def topup(self,amount='20.00'):
        return start_topup(self.user,Decimal(amount),uuid.uuid4())

    def purchase(self,quantity=5):
        wish=MovieWish.objects.filter(title='New Story').first() or self.wish()
        return create_purchase(self.manager,{'wish':wish,'movie':None,'genre':self.genre,'barcode':'1234567891','daily_rate':Decimal('4.00'),'quantity':quantity,'unit_cost':Decimal('8.00'),'supplier':'Demo supplier'},uuid.uuid4())

    def test_customer_cannot_return_even_own_rental(self):
        order=checkout(self.user,self.c.pk,{self.movie.pk:1},7,uuid.uuid4())
        with self.assertRaises(PermissionDenied):
            settle(self.user,order.pk,{order.items.get().pk:(1,0)},None,'cash',uuid.uuid4())
        self.client.force_login(self.user)
        response=self.client.get(f'/rentals/{order.pk}/')
        self.assertContains(response,'Please return your discs in store.')
        self.assertNotContains(response,'name="return_')
        self.assertNotContains(response,'Confirm return & settle')
        response=self.client.post(f'/rentals/{order.pk}/',{'request_key':str(uuid.uuid4()),f'return_{order.items.get().pk}':1})
        self.assertEqual(response.status_code,403)
        self.assertEqual(ReturnRecord.objects.count(),0)
        self.movie.refresh_from_db();self.assertEqual(self.movie.number_in_stock,4)

    def test_staff_returns_and_does_not_double_award_points(self):
        order=checkout(self.user,self.c.pk,{self.movie.pk:1},7,uuid.uuid4())
        self.client.force_login(self.cashier)
        r=self.client.post(f'/rentals/{order.pk}/',{'request_key':str(uuid.uuid4()),f'return_{order.items.get().pk}':1,'payment':'cash'})
        self.assertEqual(r.status_code,302)
        self.c.refresh_from_db();self.assertEqual(self.c.points,0)
        self.assertTrue(order.closed)

    def test_wish_dedup_and_independent_supporters(self):
        a=self.wish(title='  New   Story ')
        b=self.wish(title='new story')
        c=self.wish(self.other,title='NEW STORY')
        self.assertEqual(a.pk,b.pk);self.assertEqual(a.pk,c.pk)
        self.assertEqual(a.requests.count(),2)
        self.client.force_login(self.user)
        self.assertContains(self.client.get('/wishes/'),'2 customers interested')

    def test_wish_different_year_is_distinct(self):
        a=self.wish(year=2020);b=self.wish(year=2025);self.assertNotEqual(a.pk,b.pk)

    def test_existing_catalog_title_rejected(self):
        with self.assertRaises(BusinessError):self.wish(title='EXISTING',year=2000)

    def test_wish_web_submission(self):
        self.client.force_login(self.user)
        r=self.client.post('/wishes/',{'title':'Arrival','release_year':2016,'note':'Sci-fi'})
        self.assertEqual(r.status_code,302);self.assertTrue(MovieWish.objects.filter(title='Arrival').exists())

    def test_wish_summary_manager_only(self):
        self.wish()
        for user in [self.user,self.cashier]:
            self.client.force_login(user);self.assertEqual(self.client.get('/desk/wishes/').status_code,403)
        self.client.force_login(self.manager);self.assertContains(self.client.get('/desk/wishes/'),'New Story')

    def test_decline_shared_with_customer_and_replan_allowed(self):
        wish=self.wish();decline_wish(self.manager,wish.pk,'Not currently available')
        self.client.force_login(self.user);self.assertContains(self.client.get('/wishes/'),'Not currently available')
        order=self.purchase();wish.refresh_from_db();self.assertEqual(wish.status,'planned')
        with self.assertRaises(BusinessError):decline_wish(self.manager,wish.pk,'no')

    def test_purchase_no_stock_before_receipt(self):
        p=self.purchase();self.assertEqual(p.movie.number_in_stock,0);self.assertFalse(p.movie.active)
        p.wish.refresh_from_db();self.assertEqual(p.wish.status,'planned')
        self.client.force_login(self.user);self.assertNotContains(self.client.get('/movies/'),'New Story')

    def test_cashier_and_manager_partial_receipt(self):
        p=self.purchase();key=uuid.uuid4()
        a=receive_purchase(self.cashier,p.pk,2,key);b=receive_purchase(self.cashier,p.pk,2,key)
        self.assertEqual(a.pk,b.pk)
        p.refresh_from_db();self.assertEqual(p.remaining,3)
        p.movie.refresh_from_db();self.assertEqual((p.movie.total_quantity,p.movie.number_in_stock),(2,2))
        p.wish.refresh_from_db();self.assertEqual(p.wish.status,'available')
        receive_purchase(self.manager,p.pk,3,uuid.uuid4());p.refresh_from_db();self.assertEqual(p.remaining,0)
        self.assertEqual(StockReceipt.objects.count(),2)

    def test_overreceipt_rejected_atomically(self):
        p=self.purchase()
        with self.assertRaises(BusinessError):receive_purchase(self.cashier,p.pk,6,uuid.uuid4())
        p.movie.refresh_from_db();self.assertEqual(p.movie.total_quantity,0);self.assertFalse(StockReceipt.objects.exists())

    def test_customer_cannot_receive_or_cashier_plan(self):
        p=self.purchase()
        with self.assertRaises(PermissionDenied):receive_purchase(self.user,p.pk,1,uuid.uuid4())
        with self.assertRaises(PermissionDenied):create_purchase(self.cashier,{},uuid.uuid4())
        self.client.force_login(self.user);self.assertEqual(self.client.post(f'/desk/purchases/{p.pk}/',{}).status_code,403)
        self.client.force_login(self.cashier);self.assertEqual(self.client.get('/desk/purchases/new/').status_code,403)

    def test_receipt_key_cannot_apply_to_other_purchase(self):
        p=self.purchase();key=uuid.uuid4();receive_purchase(self.cashier,p.pk,1,key)
        other=self.purchase()
        with self.assertRaises(PermissionDenied):receive_purchase(self.cashier,other.pk,1,key)

    def test_restock_preserves_outstanding_rentals(self):
        checkout(self.user,self.c.pk,{self.movie.pk:2},7,uuid.uuid4())
        p=create_purchase(self.manager,{'movie':self.movie,'quantity':3,'unit_cost':Decimal(1),'supplier':''},uuid.uuid4())
        receive_purchase(self.cashier,p.pk,3,uuid.uuid4());self.movie.refresh_from_db()
        self.assertEqual((self.movie.total_quantity,self.movie.number_in_stock),(8,6))

    def test_purchase_web_new_and_receipt(self):
        w=self.wish();self.client.force_login(self.manager)
        data={'wish':w.pk,'genre':self.genre.pk,'barcode':'1234567891','daily_rate':'4.00','quantity':3,'unit_cost':'7.00','request_key':str(uuid.uuid4())}
        r=self.client.post('/desk/purchases/new/',data);self.assertEqual(r.status_code,302)
        p=PurchaseOrder.objects.get();self.client.force_login(self.cashier)
        r=self.client.post(f'/desk/purchases/{p.pk}/',{'quantity':2,'request_key':str(uuid.uuid4())})
        self.assertEqual(r.status_code,302);p.movie.refresh_from_db();self.assertEqual(p.movie.number_in_stock,2)

    def test_topup_pending_has_no_money_or_points(self):
        self.topup();self.c.refresh_from_db()
        self.assertEqual(self.c.balance,0);self.assertEqual(self.c.points,0);self.assertFalse(Ledger.objects.exists())

    def test_success_credit_once(self):
        order=self.topup();finish_topup(self.user,order.pk,'success');finish_topup(self.user,order.pk,'success')
        self.c.refresh_from_db();self.assertEqual(self.c.balance,20);self.assertEqual(self.c.points,200)
        self.assertEqual(Ledger.objects.count(),1);self.assertEqual(PointsEntry.objects.count(),1)

    def test_failure_cancel_and_no_replay_success(self):
        for outcome in ['failed','cancelled']:
            order=self.topup();finish_topup(self.user,order.pk,outcome);finish_topup(self.user,order.pk,'success')
        self.c.refresh_from_db();self.assertEqual(self.c.balance,0);self.assertEqual(self.c.points,0)

    def test_topup_ownership_including_manager(self):
        order=self.topup()
        for user in [self.other,self.manager]:
            with self.assertRaises(PermissionDenied):finish_topup(user,order.pk,'success')
            self.client.force_login(user);self.assertEqual(self.client.get(f'/wallet/pay/{order.pk}/').status_code,403)

    def test_snapshot_and_fractional_rounding(self):
        configure_rewards(self.manager,Decimal('3'),10,True)
        order=self.topup('2.00');self.assertEqual(order.awarded_points,6)
        configure_rewards(self.superuser,Decimal('1'),100,True)
        finish_topup(self.user,order.pk,'success');self.c.refresh_from_db();self.assertEqual(self.c.points,6)
        self.assertEqual(PolicyRevision.objects.count(),2)

    def test_closed_topup_and_pending_snapshot(self):
        order=self.topup();configure_rewards(self.manager,Decimal(1),10,False)
        with self.assertRaises(BusinessError):self.topup()
        finish_topup(self.user,order.pk,'success');self.c.refresh_from_db();self.assertEqual(self.c.balance,20)

    def test_expired_order_cannot_credit(self):
        order=self.topup();order.created_at=timezone.now()-timedelta(minutes=31);order.save()
        result=finish_topup(self.user,order.pk,'success');self.assertEqual(result.status,'expired');self.assertFalse(Ledger.objects.exists())

    def test_invalid_amounts_and_policy(self):
        for amount in ['0','-1','10000.01','1.001','NaN','Infinity']:
            with self.subTest(amount=amount),self.assertRaises(BusinessError):self.topup(amount)
        with self.assertRaises(ValidationError):configure_rewards(self.manager,Decimal('0'),10,True)

    def test_policy_permission_web_and_superuser(self):
        for user in [self.user,self.cashier]:
            with self.assertRaises(PermissionDenied):configure_rewards(user,Decimal(1),10,True)
            self.client.force_login(user);self.assertEqual(self.client.post('/desk/settings/rewards/',{}).status_code,403)
        for user in [self.manager,self.superuser]:
            self.client.force_login(user)
            self.assertEqual(self.client.post('/desk/settings/rewards/',{'money_unit':'10','points_unit':100,'enabled':'on'}).status_code,302)
        self.assertEqual(RewardPolicy.objects.get().points_unit,100)

    def test_topup_key_idempotent_owner_checked(self):
        key=uuid.uuid4();a=start_topup(self.user,Decimal(20),key);b=start_topup(self.user,Decimal(200),key)
        self.assertEqual(a.pk,b.pk);self.assertEqual(b.amount,20)
        with self.assertRaises(PermissionDenied):start_topup(self.other,Decimal(20),key)

    def test_payment_client_amount_tampering_ignored(self):
        self.client.force_login(self.user)
        r=self.client.post('/wallet/',{'amount':'12.50','request_key':str(uuid.uuid4())});self.assertEqual(r.status_code,302)
        order=TopUp.objects.get()
        self.client.post(f'/wallet/pay/{order.pk}/',{'outcome':'success','amount':'99999','awarded_points':'99999'})
        self.c.refresh_from_db();self.assertEqual(self.c.balance,Decimal('12.50'));self.assertEqual(self.c.points,125)

    def test_partial_refunds_reverse_original_points_cumulatively(self):
        configure_rewards(self.manager,Decimal(3),10,True)
        order=self.topup('3.00');finish_topup(self.user,order.pk,'success')
        configure_rewards(self.manager,Decimal(1),100,True)
        adjust_balance(self.cashier,self.c.pk,Decimal(1),'refund',uuid.uuid4())
        self.c.refresh_from_db();self.assertEqual(self.c.points,7)
        key=uuid.uuid4();adjust_balance(self.cashier,self.c.pk,Decimal(2),'refund',key);adjust_balance(self.cashier,self.c.pk,Decimal(2),'refund',key)
        self.c.refresh_from_db();self.assertEqual(self.c.balance,0);self.assertEqual(self.c.points,0)
        order.refresh_from_db();self.assertEqual(order.reversed_points,10)

    def test_customer_topup_rejected_if_account_inactive(self):
        self.c.active=False;self.c.save()
        with self.assertRaises(BusinessError):self.topup()

    def test_new_pages_render_and_csrf(self):
        self.client.force_login(self.user)
        for path in ['/wallet/','/wishes/']:
            self.assertEqual(self.client.get(path).status_code,200)
        p=self.purchase();order=self.topup()
        self.assertEqual(self.client.get(f'/wallet/pay/{order.pk}/').status_code,200)
        self.client.force_login(self.manager)
        for path in ['/desk/purchases/','/desk/purchases/new/',f'/desk/purchases/{p.pk}/',f'/desk/wishes/{p.wish_id}/','/desk/settings/rewards/']:
            self.assertEqual(self.client.get(path).status_code,200)
        secure=Client(enforce_csrf_checks=True);secure.force_login(self.user)
        self.assertEqual(secure.post(f'/wallet/pay/{order.pk}/',{'outcome':'success'}).status_code,403)

    def test_admin_configuration_uses_same_audit_service(self):
        configure_rewards(self.manager,Decimal(1),10,True)
        for user in [self.manager,self.superuser]:
            self.client.force_login(user)
            self.assertEqual(self.client.get('/admin/rentals/rewardpolicy/1/change/').status_code,200)
            r=self.client.post('/admin/rentals/rewardpolicy/1/change/',{'money_unit':'5.00','points_unit':'40','enabled':'on','_save':'Save'})
            self.assertEqual(r.status_code,302)
        self.assertEqual(RewardPolicy.objects.get().points_unit,40)
        self.assertEqual(PolicyRevision.objects.count(),3)
        self.client.force_login(self.cashier)
        self.assertEqual(self.client.get('/admin/rentals/rewardpolicy/1/change/').status_code,403)

    def test_bootstrap_preserves_existing_catalog(self):
        from django.core.management import call_command
        from io import StringIO
        call_command('setup_demo',only_empty=True,accounts=True,stdout=StringIO())
        self.assertEqual(Movie.objects.count(),1)
        self.assertFalse(User.objects.filter(username='demo').exists())

    def test_purchased_movie_cannot_be_hard_deleted(self):
        p=self.purchase();self.client.force_login(self.manager)
        self.assertEqual(self.client.post(f'/desk/inventory/{p.movie_id}/delete/').status_code,302)
        self.assertTrue(Movie.objects.filter(pk=p.movie_id).exists())

    def test_matching_wish_can_gain_support_while_waiting_for_arrival(self):
        p=self.purchase()
        self.wish(self.other)
        self.assertEqual(p.wish.requests.count(),2)

    def test_payment_get_does_not_charge(self):
        order=self.topup();self.client.force_login(self.user)
        self.client.get(f'/wallet/pay/{order.pk}/?outcome=success')
        order.refresh_from_db();self.assertEqual(order.status,'pending');self.assertFalse(Ledger.objects.exists())
