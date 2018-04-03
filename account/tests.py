from django.test import TestCase
from django.test import TestCase
from django.contrib.auth import models as dmod
from account import models as amod
import datetime


class UserModelTest(TestCase):

    fixtures = [ 'data.yaml' ]

    def setUp(self):
        self.u1 = amod.User()
        self.u1.first_name = "Marge"
        self.u1.last_name = "Simpson"
        self.u1.email = "marge@simpsons.com"
        self.u1.set_password('password')
        self.u1.is_staff = True
        self.u1.is_active = True
        self.u1.last_login = datetime.date.today()
        self.u1.date_joined = datetime.date.today()
        self.u1.address = "This is an address"
        self.u1.city = "This is a city"
        self.u1.state = "This is a state"
        self.u1.zip = "11111"
        self.u1.save()

    def test_user_create_save_load(self):
        '''Tests round trip of user model to from database'''
        u2 = amod.User.objects.get(email=self.u1.email)
        self.assertEquals(self.u1.first_name, u2.first_name)
        self.assertEquals(self.u1.last_name, u2.last_name)
        self.assertEquals(self.u1.email, u2.email)
        self.assertEquals(self.u1.password, u2.password)
        self.assertEquals(self.u1.is_staff, u2.is_staff)
        self.assertEquals(self.u1.is_active, u2.is_active)
        self.assertEquals(self.u1.last_login.year, u2.last_login.year)
        self.assertEquals(self.u1.last_login.month, u2.last_login.month)
        self.assertEquals(self.u1.last_login.day, u2.last_login.day)
        self.assertEquals(self.u1.date_joined.year, u2.date_joined.year)
        self.assertEquals(self.u1.date_joined.month, u2.date_joined.month)
        self.assertEquals(self.u1.date_joined.day, u2.date_joined.day)
        self.assertEquals(self.u1.address, u2.address)
        self.assertEquals(self.u1.city, u2.city)
        self.assertEquals(self.u1.state, u2.state)
        self.assertEquals(self.u1.zip, u2.zip)
        self.assertEquals(self.u1.is_authenticated, u2.is_authenticated)
        self.assertEquals(self.u1.is_anonymous, u2.is_anonymous)


    def test_groups(self):
        '''Makes sure that permissions can be accessed through groups.'''
        u2 = amod.User()
        u2.first_name = "Gerald"
        u2.last_name = "Ford"
        u2.email = "VP2POTUS@whitehouse.com"
        u2.set_password('richNixon')
        u2.is_staff = True
        u2.is_active = True
        u2.last_login = datetime.date.today() + datetime.timedelta(days = -5392)
        u2.date_joined = datetime.date.today() + datetime.timedelta(days = -2395)
        u2.address = "My address"
        u2.city = "My city"
        u2.state = "My state"
        u2.zip = "22222"
        u2.save()
        p1 = dmod.Permission.objects.get(id = 1)
        p2 = dmod.Permission.objects.get(id = 2)
        p3 = dmod.Permission.objects.get(id = 101)
        g1 = dmod.Group()
        g1.name = "Awesome Users"
        g1.save()
        g1.permissions.set([p1, p2])
        g1.save()
        gr2 = dmod.Group()
        gr2.name = "Other Users"
        gr2.save()
        gr2.permissions.set([p2, p3])
        gr2.save()
        self.u1.groups.add(g1)
        self.u1.save()
        u2.groups.add(gr2)
        u2.save()
        self.assertTrue(self.u1.has_perm(p1.content_type.app_label + "." + p1.codename))
        self.assertTrue(self.u1.has_perm(p2.content_type.app_label + "." + p2.codename))
        self.assertFalse(self.u1.has_perm(p3.content_type.app_label + "." + p3.codename))
        self.assertFalse(u2.has_perm(p1.content_type.app_label + "." + p1.codename))
        self.assertTrue(u2.has_perm(p2.content_type.app_label + "." + p2.codename))
        self.assertTrue(u2.has_perm(p3.content_type.app_label + "." + p3.codename))



    def test_permissions(self):
        '''Makes sure that permissions can be accessed through users.'''
        u2 = amod.User()
        u2.first_name = "Gerald"
        u2.last_name = "Ford"
        u2.email = "VP2POTUS@whitehouse.com"
        u2.set_password('richNixon')
        u2.is_staff = True
        u2.is_active = True
        u2.last_login = datetime.date.today() + datetime.timedelta(days = -5392)
        u2.date_joined = datetime.date.today() + datetime.timedelta(days = -2395)
        u2.address = "My address"
        u2.city = "My city"
        u2.state = "My state"
        u2.zip = "22222"
        u2.save()
        p1 = dmod.Permission.objects.get(id = 1)
        p2 = dmod.Permission.objects.get(id = 2)
        p3 = dmod.Permission.objects.get(id = 101)
        self.u1.user_permissions.set([p1, p2])
        self.u1.save()
        u2.user_permissions.set([p2, p3])
        u2.save()
        self.assertTrue(self.u1.has_perm(p1.content_type.app_label + "." + p1.codename))
        self.assertTrue(self.u1.has_perm(p2.content_type.app_label + "." + p2.codename))
        self.assertFalse(self.u1.has_perm(p3.content_type.app_label + "." + p3.codename))
        self.assertFalse(u2.has_perm(p1.content_type.app_label + "." + p1.codename))
        self.assertTrue(u2.has_perm(p2.content_type.app_label + "." + p2.codename))
        self.assertTrue(u2.has_perm(p3.content_type.app_label + "." + p3.codename))

    #def test_login(self):
        '''Test to make sure that logging in functions properly'''

    #def test_logout(self):
        '''Test to make sure that logging out functions properly'''

    def test_passwords(self):
        '''Test to make sure that passwords function correctly'''
        u1 = amod.User()
        u1.set_password('password')
        u1.save()
        u2 = amod.User.objects.get(email=u1.email)
        self.assertTrue(u2.check_password("password"))

    def test_changing_information(self):
        '''Test to make sure that changing information can work'''
        u2 = amod.User.objects.get(email=self.u1.email)
        u2.first_name = "Gerald"
        u2.last_name = "Ford"
        u2.email = "VP2POTUS@whitehouse.com"
        u2.set_password('richNixon')
        u2.is_staff = False
        u2.is_active = False
        u2.last_login = datetime.date.today() + datetime.timedelta(days = -5392)
        u2.date_joined = datetime.date.today() + datetime.timedelta(days = -2395)
        u2.address = "My address"
        u2.city = "My city"
        u2.state = "My state"
        u2.zip = "22222"
        u2.save()
        u3 = amod.User.objects.get(email=u2.email)
        self.assertEquals(u2.first_name, u3.first_name)
        self.assertEquals(u2.last_name, u3.last_name)
        self.assertEquals(u2.email, u3.email)
        self.assertEquals(u2.password, u3.password)
        self.assertEquals(u2.is_staff, u3.is_staff)
        self.assertEquals(u2.is_active, u3.is_active)
        self.assertEquals(u2.last_login.year, u3.last_login.year)
        self.assertEquals(u2.last_login.month, u3.last_login.month)
        self.assertEquals(u2.last_login.day, u3.last_login.day)
        self.assertEquals(u2.date_joined.year, u3.date_joined.year)
        self.assertEquals(u2.date_joined.month, u3.date_joined.month)
        self.assertEquals(u2.date_joined.day, u3.date_joined.day)
        self.assertEquals(u2.address, u3.address)
        self.assertEquals(u2.city, u3.city)
        self.assertEquals(u2.state, u3.state)
        self.assertEquals(u2.zip, u3.zip)
