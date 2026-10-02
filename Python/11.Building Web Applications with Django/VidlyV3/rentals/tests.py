import uuid
from decimal import Decimal
from datetime import timedelta
from django.test import TestCase,Client,override_settings
from django.contrib.auth.models import User,Group
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from movies.models import Movie,Genre
from .models import Customer,Rental,RentalItem,ReturnRecord,Coupon,CustomerCoupon,Ledger
from .services import checkout,settle,adjust_balance,BusinessError

@override_settings(STORAGES={'default':{'BACKEND':'django.core.files.storage.FileSystemStorage'},'staticfiles':{'BACKEND':'django.contrib.staticfiles.storage.StaticFilesStorage'}})
class BusinessTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.u=User.objects.create_user('alice',password='ComplexPass!993')
        cls.other=User.objects.create_user('bob',password='ComplexPass!993')
        cls.customer=Customer.objects.create(user=cls.u,full_name='Alice',phone='+4912345678')
        cls.other_customer=Customer.objects.create(user=cls.other,full_name='Bob',phone='+4912345679')
        cls.cashier=User.objects.create_user('cashier',password='ComplexPass!993',is_staff=True)
        cls.cashier.groups.add(Group.objects.create(name='Cashier'))
        cls.manager=User.objects.create_user('manager',password='ComplexPass!993',is_staff=True)
        cls.manager.groups.add(Group.objects.create(name='Manager'))
        cls.g=Genre.objects.create(name='Drama')
        cls.movie=Movie.objects.create(title='Test Film',genre=cls.g,release_year=1994,number_in_stock=5,total_quantity=5,daily_rate=Decimal('2.50'),barcode='1000000001')
        cls.second=Movie.objects.create(title='Other Film',genre=cls.g,release_year=1999,number_in_stock=1,total_quantity=1,daily_rate=Decimal('3.00'),barcode='1000000002')
    def order(self,qty=2):return checkout(self.u,self.customer.pk,{self.movie.pk:qty},7,uuid.uuid4())
    def item(self,order):return order.items.get()
    def test_checkout_stock_and_price_snapshot(self):
        o=self.order();self.movie.refresh_from_db();self.assertEqual(self.movie.number_in_stock,3)
        self.movie.daily_rate=9;self.movie.save();self.assertEqual(self.item(o).daily_rate,Decimal('2.50'))
    def test_checkout_is_idempotent(self):
        key=uuid.uuid4();a=checkout(self.u,self.customer.pk,{self.movie.pk:1},7,key);b=checkout(self.u,self.customer.pk,{},7,key)
        self.assertEqual(a.pk,b.pk);self.movie.refresh_from_db();self.assertEqual(self.movie.number_in_stock,4)
    def test_entire_order_rolls_back_on_stock_failure(self):
        with self.assertRaises(BusinessError):checkout(self.u,self.customer.pk,{self.movie.pk:2,self.second.pk:2},7,uuid.uuid4())
        self.movie.refresh_from_db();self.assertEqual(self.movie.number_in_stock,5);self.assertEqual(Rental.objects.count(),0)
    def test_last_copy_cannot_be_oversold(self):
        checkout(self.u,self.customer.pk,{self.second.pk:1},7,uuid.uuid4())
        with self.assertRaises(BusinessError):checkout(self.other,self.other_customer.pk,{self.second.pk:1},7,uuid.uuid4())
    def test_inactive_movie_rejected(self):
        self.movie.active=False;self.movie.save()
        with self.assertRaises(BusinessError):self.order()
    def test_inactive_customer_rejected(self):
        self.customer.active=False;self.customer.save()
        with self.assertRaises(BusinessError):self.order()
    def test_checkout_ownership(self):
        with self.assertRaises(PermissionDenied):checkout(self.other,self.customer.pk,{self.movie.pk:1},7,uuid.uuid4())
    def test_partial_return_and_remaining(self):
        o=self.order();i=self.item(o);r=settle(self.cashier,o.pk,{i.pk:(1,0)},None,'cash',uuid.uuid4())
        self.assertEqual(r.amount,Decimal('2.50'));i.refresh_from_db();self.assertEqual(i.remaining,1);self.assertFalse(o.closed)
        self.movie.refresh_from_db();self.assertEqual(self.movie.number_in_stock,4)
    def test_lost_reduces_total_not_available(self):
        o=self.order();i=self.item(o);r=settle(self.cashier,o.pk,{i.pk:(0,1)},None,'cash',uuid.uuid4())
        self.assertEqual(r.amount,Decimal('12.50'));self.movie.refresh_from_db();self.assertEqual((self.movie.number_in_stock,self.movie.total_quantity),(3,4))
    def test_repeat_return_rejected(self):
        o=self.order(1);i=self.item(o);settle(self.cashier,o.pk,{i.pk:(1,0)},None,'cash',uuid.uuid4())
        with self.assertRaises(BusinessError):settle(self.cashier,o.pk,{i.pk:(1,0)},None,'cash',uuid.uuid4())
        self.movie.refresh_from_db();self.assertEqual(self.movie.number_in_stock,5)
    def test_return_idempotency(self):
        o=self.order();i=self.item(o);key=uuid.uuid4();a=settle(self.cashier,o.pk,{i.pk:(1,0)},None,'cash',key);b=settle(self.cashier,o.pk,{i.pk:(1,0)},None,'cash',key)
        self.assertEqual(a.pk,b.pk);self.assertEqual(ReturnRecord.objects.count(),1)
    def test_cross_order_idempotency_key_forbidden(self):
        o=self.order(1);r=settle(self.cashier,o.pk,{self.item(o).pk:(1,0)},None,'cash',uuid.uuid4());o2=self.order(1)
        with self.assertRaises(PermissionDenied):settle(self.cashier,o2.pk,{self.item(o2).pk:(1,0)},None,'cash',r.request_key)
    def test_rounds_up_actual_days(self):
        o=self.order(1);o.created_at=timezone.now()-timedelta(days=1,hours=1);o.save();r=settle(self.cashier,o.pk,{self.item(o).pk:(1,0)},None,'cash',uuid.uuid4())
        self.assertEqual(r.amount,Decimal('5.00'))
    def coupon(self,customer=None,**kw):
        c=Coupon.objects.create(code='TEN',name='10 percent',percent=10,**kw)
        return CustomerCoupon.objects.create(customer=customer or self.customer,coupon=c)
    def test_coupon_only_rental_not_lost(self):
        cc=self.coupon();o=self.order();r=settle(self.cashier,o.pk,{self.item(o).pk:(1,1)},cc.pk,'cash',uuid.uuid4())
        self.assertEqual(r.amount,Decimal('14.75'));cc.refresh_from_db();self.assertIsNotNone(cc.used_at)
    def test_used_coupon_rejected(self):
        cc=self.coupon();o=self.order();settle(self.cashier,o.pk,{self.item(o).pk:(1,0)},cc.pk,'cash',uuid.uuid4())
        with self.assertRaises(BusinessError):settle(self.cashier,o.pk,{self.item(o).pk:(1,0)},cc.pk,'cash',uuid.uuid4())
    def test_expired_coupon_rejected(self):
        cc=self.coupon(expires_at=timezone.now()-timedelta(days=1));o=self.order()
        with self.assertRaises(BusinessError):settle(self.cashier,o.pk,{self.item(o).pk:(1,0)},cc.pk,'cash',uuid.uuid4())
    def test_other_customer_coupon_rejected(self):
        cc=self.coupon(customer=self.other_customer);o=self.order()
        with self.assertRaises(BusinessError):settle(self.cashier,o.pk,{self.item(o).pk:(1,0)},cc.pk,'cash',uuid.uuid4())
    def test_insufficient_balance_rolls_back_return(self):
        o=self.order();i=self.item(o)
        with self.assertRaises(BusinessError):settle(self.cashier,o.pk,{i.pk:(1,0)},None,'balance',uuid.uuid4())
        i.refresh_from_db();self.assertEqual(i.remaining,2);self.assertEqual(ReturnRecord.objects.count(),0)
    def test_wallet_recharge_settle_refund(self):
        key=uuid.uuid4();adjust_balance(self.cashier,self.customer.pk,20,'recharge',key);adjust_balance(self.cashier,self.customer.pk,20,'recharge',key)
        o=self.order(1);settle(self.cashier,o.pk,{self.item(o).pk:(1,0)},None,'balance',uuid.uuid4());adjust_balance(self.cashier,self.customer.pk,5,'refund',uuid.uuid4())
        self.customer.refresh_from_db();self.assertEqual(self.customer.balance,Decimal('12.50'));self.assertEqual(Ledger.objects.count(),3)
    def test_refund_cannot_exceed_balance(self):
        with self.assertRaises(BusinessError):adjust_balance(self.cashier,self.customer.pk,5,'refund',uuid.uuid4())
    def test_customer_cannot_recharge(self):
        with self.assertRaises(PermissionDenied):adjust_balance(self.u,self.customer.pk,100,'recharge',uuid.uuid4())
    def test_customer_cannot_see_others_order(self):
        o=self.order();self.client.force_login(self.other);self.assertEqual(self.client.get(f'/rentals/{o.pk}/').status_code,403)
    def test_role_permissions(self):
        self.client.force_login(self.u);self.assertEqual(self.client.get('/desk/').status_code,403)
        self.client.force_login(self.cashier);self.assertEqual(self.client.get('/desk/').status_code,200);self.assertEqual(self.client.get('/desk/inventory/').status_code,403);self.assertEqual(self.client.get('/desk/reports/').status_code,403)
        self.client.force_login(self.manager);self.assertEqual(self.client.get('/desk/inventory/').status_code,200);self.assertEqual(self.client.get('/desk/reports/').status_code,200)
    def test_public_pages_and_api(self):
        for path in ['/','/movies/','/movies/?q=Test','/movies/?genre=1','/movies/?sort=price','/movies/?page=99','/movies/1/','/bag/','/accounts/login/','/accounts/signup/','/api/movies/']:
            with self.subTest(path=path):self.assertEqual(self.client.get(path).status_code,200)
        self.assertEqual(self.client.post('/api/movies/').status_code,405)
    def test_mutations_require_post(self):
        for path in ['/bag/add/1/','/bag/update/1/']:
            self.assertEqual(self.client.get(path).status_code,405)
    def test_csrf_enforced(self):
        client=Client(enforce_csrf_checks=True);client.force_login(self.u)
        self.assertEqual(client.post('/bag/add/1/').status_code,403)
    def test_signup_and_checkout_web(self):
        response=self.client.post('/accounts/signup/',{'username':'newuser','full_name':'New User','phone':'+49 555 99999','email':'new@example.com','password1':'ComplexPass!993','password2':'ComplexPass!993'})
        self.assertEqual(response.status_code,302);self.assertTrue(Customer.objects.filter(phone='+4955599999').exists())
        self.client.post('/bag/add/1/');r=self.client.post('/checkout/',{'days':3,'request_key':str(uuid.uuid4())});self.assertEqual(r.status_code,302);self.assertEqual(Rental.objects.count(),1)
    def test_coupon_claim_once(self):
        Coupon.objects.create(code='WELCOME10',name='welcome',percent=10);self.client.force_login(self.u)
        for _ in range(2):self.client.post('/coupons/claim/',{'code':'WELCOME10'})
        self.assertEqual(CustomerCoupon.objects.count(),1)
    def test_counter_multi_movie_barcode(self):
        self.client.force_login(self.cashier);r=self.client.post('/desk/checkout/',{'customer':self.customer.pk,'barcodes':'1000000001 2\n1000000002','days':7,'request_key':str(uuid.uuid4())})
        self.assertEqual(r.status_code,302);self.assertEqual(RentalItem.objects.count(),2)
    def test_cannot_reduce_stock_below_outstanding(self):
        self.order(3);self.client.force_login(self.manager)
        data={'title':'Test','release_year':1994,'genre':self.g.pk,'daily_rate':'2.50','total_quantity':2,'barcode':'1000000001','runtime':120,'active':'on'}
        r=self.client.post('/desk/inventory/1/',data);self.assertEqual(r.status_code,200);self.movie.refresh_from_db();self.assertEqual(self.movie.total_quantity,5)
    def test_historical_movie_soft_delete(self):
        self.order();self.client.force_login(self.manager);self.client.post('/desk/inventory/1/delete/');self.movie.refresh_from_db();self.assertFalse(self.movie.active)
    def test_report_excludes_recharges(self):
        adjust_balance(self.cashier,self.customer.pk,100,'recharge',uuid.uuid4());o=self.order(1);settle(self.cashier,o.pk,{self.item(o).pk:(1,0)},None,'cash',uuid.uuid4())
        self.client.force_login(self.manager)
        for period in ['day','month','year']:
            r=self.client.get('/desk/reports/',{'period':period});self.assertEqual(r.context['total_revenue'],Decimal('2.50'));self.assertEqual(r.status_code,200)
    def test_staff_forms_render(self):
        self.client.force_login(self.manager)
        for path in ['/desk/customers/','/desk/customers/new/','/desk/customers/1/edit/','/desk/customers/1/wallet/','/desk/checkout/','/desk/inventory/new/','/desk/inventory/1/']:
            with self.subTest(path=path):self.assertEqual(self.client.get(path).status_code,200)
    def test_return_detail_template(self):
        o=self.order();self.client.force_login(self.u);self.assertEqual(self.client.get(f'/rentals/{o.pk}/').status_code,200)
        self.assertEqual(self.client.post(f'/rentals/{o.pk}/',{'return_1':1,'lost_1':0,'payment':'cash','request_key':str(uuid.uuid4())}).status_code,403)
        self.assertEqual(self.client.get(f'/rentals/{o.pk}/').status_code,200)

    def test_deleted_cart_movie_returns_business_error(self):
        mid=self.second.pk
        self.second.delete()
        with self.assertRaises(BusinessError):
            checkout(self.u,self.customer.pk,{mid:1},7,uuid.uuid4())
        self.assertFalse(Rental.objects.exists())

    def test_report_money_uses_two_decimal_places(self):
        o=self.order(1);i=self.item(o)
        settle(self.cashier,o.pk,{i.pk:(1,0)},None,'cash',uuid.uuid4())
        self.client.force_login(self.manager)
        response=self.client.get('/desk/reports/')
        self.assertContains(response,'€2.50')
        self.assertNotContains(response,'2.500000')
