import importlib
import re
from types import SimpleNamespace
from django.apps import apps
from django.contrib.auth.models import Group, User, Permission
from django.core.management import call_command
from django.db import connection
from django.test import TestCase, override_settings
from django.urls import reverse
from movies.models import Movie
from .models import Customer, Coupon
from .services import is_manager, is_staff


@override_settings(STORAGES={'default':{'BACKEND':'django.core.files.storage.FileSystemStorage'},'staticfiles':{'BACKEND':'django.contrib.staticfiles.storage.StaticFilesStorage'}})
class EnglishExperienceTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        with override_settings(DEBUG=True):
            call_command('setup_demo', accounts=True, verbosity=0)

    def test_public_qa_content_and_links(self):
        response = self.client.get(reverse('qa'))
        self.assertEqual(response.status_code, 200)
        for text in ['Ryandou, a product manager', 'database modelling', 'AI', 'physical movie-disc rental', 'Only a cashier or manager', 'WELCOME10', 'No bank card', 'Revenue', '<details open>', '<html lang="en">']:
            self.assertContains(response, text)
        html = response.content.decode()
        self.assertGreaterEqual(html.count('<summary>'), 12)
        for target in re.findall(r'href="(#[^"]+)"', html):
            self.assertIn('id="'+target[1:]+'"', html)
        for target in set(re.findall(r'href="(/[^"#]*)"', html)):
            self.assertIn(self.client.get(target).status_code, [200,302], target)

    def test_english_for_all_roles_including_admin(self):
        public = ['/', '/movies/', '/movies/1/', '/bag/', '/qa/', '/accounts/login/', '/accounts/signup/', '/does-not-exist/']
        customer = ['/rentals/', '/wishes/', '/wallet/']
        staff = ['/desk/', '/desk/customers/', '/desk/customers/new/', '/desk/customers/3/wallet/', '/desk/checkout/', '/desk/purchases/']
        manager = ['/desk/wishes/', '/desk/settings/rewards/', '/desk/purchases/new/', '/desk/inventory/', '/desk/inventory/new/', '/desk/reports/', '/admin/', '/admin/rentals/coupon/', '/admin/rentals/coupon/add/']
        for username, paths in [(None,public),('demo',customer),('cashier',staff),('manager',staff+manager)]:
            if username:self.client.force_login(User.objects.get(username=username))
            for path in paths:
                response=self.client.get(path)
                self.assertEqual(response.status_code,404 if path=='/does-not-exist/' else 200,(username,path))
                self.assertIsNone(re.search(r'[\u4e00-\u9fff]',response.content.decode()),(username,path))
                self.assertContains(response,'Q&amp;A') if not path.startswith('/admin/') and response.status_code==200 else None

    def test_validation_errors_are_english(self):
        response=self.client.post('/accounts/login/',{'username':'missing','password':'wrong'})
        self.assertContains(response,'Please enter a correct username and password')
        self.assertIsNone(re.search(r'[\u4e00-\u9fff]',response.content.decode()))
        self.client.force_login(User.objects.get(username='demo'))
        response=self.client.post('/wishes/',{'title':'New','release_year':1700})
        self.assertContains(response,'Ensure this value is greater than or equal to 1888')
        self.assertIsNone(re.search(r'[\u4e00-\u9fff]',response.content.decode()))

    def test_upgrade_merges_roles_and_preserves_user_data(self):
        migration=importlib.import_module('rentals.migrations.0004_translate_demo_content')
        old=Group.objects.create(name='店长')
        permission=Permission.objects.get(codename='view_customer')
        old.permissions.add(permission)
        user=User.objects.create_user('legacy-manager',is_staff=True)
        user.groups.add(old)
        cashier=User.objects.create_user('legacy-cashier',is_staff=True)
        Group.objects.filter(name='Cashier').delete()
        cashier.groups.add(Group.objects.create(name='收银员'))
        film=Movie.objects.get(pk=1)
        custom='保留用户自己编写的简介'
        film.synopsis=custom;film.save()
        customer=Customer.objects.get(user__username='demo')
        customer.balance='27.50';customer.points=19;customer.full_name='Alex · 演示客户';customer.save()
        Coupon.objects.filter(code='WELCOME10').update(name='初次相遇 · 租金 9 折')
        before=Movie.objects.values_list('pk','number_in_stock','total_quantity')
        before=list(before)
        migration.translate_existing(apps, SimpleNamespace(connection=connection))
        migration.translate_existing(apps, SimpleNamespace(connection=connection))
        self.assertTrue(is_manager(user));self.assertTrue(is_staff(cashier))
        self.assertTrue(user.groups.get(name='Manager').permissions.filter(pk=permission.pk).exists())
        self.assertFalse(Group.objects.filter(name__in=['店长','收银员']).exists())
        customer.refresh_from_db();film.refresh_from_db()
        self.assertEqual(str(customer.balance),'27.50');self.assertEqual(customer.points,19)
        self.assertEqual(customer.full_name,'Alex · Demo customer');self.assertEqual(film.synopsis,custom)
        self.assertEqual(list(Movie.objects.values_list('pk','number_in_stock','total_quantity')),before)
        self.assertEqual(Coupon.objects.get(code='WELCOME10').name,'Welcome · 10% off rental fees')
