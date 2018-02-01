# -*- coding: UTF-8 -*-
import unittest
from django.test import TestCase
from django.urls import reverse
from test_plus import APITestCase
from rest_framework import status

from repair.apps.login.models import CaseStudy, User, Profile, UserInCasestudy
from repair.apps.login.factories import (UserFactory,
                                         GroupFactory,
                                         UserInCasestudyFactory,
                                         ProfileFactory,
                                         CaseStudyFactory)
from repair.tests.test import BasicModelPermissionTest, CompareAbsURIMixin
from django.contrib.auth.models import Permission


class ModelTest(TestCase):

    def test_user_creation(self):
        # New user created
        user = User.objects.create(
            username="horst",
            password="django-tutorial",
            email='horst@gmail.com')
        # Check that a Profile instance has been crated
        self.assertIsInstance(user.profile, Profile)
        # Call the save method of the user to activate the signal
        # again, and check that it doesn't try to create another
        # profile instace
        user.save()
        self.assertIsInstance(user.profile, Profile)

    def test_profile_creation(self):
        profile = ProfileFactory()
        # should use the default username of the UserFactory
        self.assertEqual(str(profile), profile.user.username)

        # should use the provided username
        profile = ProfileFactory(user__username='Adele')
        self.assertEqual(str(profile), "Adele")

    def test_string_representation(self):
        casestudy = CaseStudy(name="Liège")
        self.assertEqual(str(casestudy), "Liège")

        user = UserFactory(username="Markus")
        self.assertEqual(str(user.profile), "Markus")

        uic = UserInCasestudy(user=user.profile, casestudy=casestudy)
        self.assertEqual(str(uic), "Markus (Liège)")

    def test_casestudies_of_profile(self):
        casestudy_hh = CaseStudyFactory(name='Hamburg')
        casestudy_ams = CaseStudyFactory(name='Amsterdam')
        casestudies = [casestudy_hh, casestudy_ams]
        user = ProfileFactory()
        user_in_hh = UserInCasestudyFactory(user=user,
                                            casestudy=casestudy_hh)
        user_in_ams = UserInCasestudyFactory(user=user,
                                             casestudy=casestudy_ams)

        # assert that the user has the correct casestudies assigned
        self.assertEqual([(cs.id, cs.name) for cs in user.casestudies.all()],
                         [(cs.id, cs.name) for cs in casestudies])


# skipped -> use admin area
class ViewTest(CompareAbsURIMixin):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.password = 'Test'
        cls.group1 = GroupFactory(name='Group1')
        cls.group2 = GroupFactory(name='Group2')
        # create the anonymus user with user_id -1
        cls.anonymus_user = ProfileFactory(user__username='Rabbit',
                                           user__password='Test',
                                           user__id=-1)
        # create a normal user
        cls.user2 = ProfileFactory(user__username='User2',
                                   user__password='Password')

        cls.casestudy = CaseStudyFactory(name='lodz')
        permissions = Permission.objects.all()
        cls.user2.user.user_permissions.set(list(permissions))
        cls.anonymus_user.user.user_permissions.set(list(permissions))

        def setUp(self):
            self.client.force_login(user=self.anonymus_user.user)
            super().setUp()

        def tearDown(self):
            self.client.logout()
            super().tearDown()


    def test_get_group(self):
        url = reverse('group-list')
        data = {'name': 'MyGroup'}
        response = self.post('group-list', data=data,
                             extra=dict(format='json'))
        self.response_201()

        response = self.get_check_200('group-list')
        results = response.data['results']
        last_entry = results[-1]
        assert last_entry['name'] == 'MyGroup'

    def test_get_user(self):

        response = self.get_check_200('user-list')
        # users before adding a new one
        no_of_users = response.data['count']

        # add new user
        lodz = self.reverse('casestudy-detail', pk=self.casestudy.pk)
        group = self.reverse('group-detail', pk=self.group1.pk)
        initial_mail = 'a.b@c.de'
        data = {'username': 'MyUser',
                'casestudies': [lodz],
                'password': 'PW',
                'organization': 'GGR',
                'groups': [group],
                'email': initial_mail, }
        response = self.post('user-list',
                             data=data,
                             extra={'format': 'json'}, )
        self.response_201()
        new_id = response.data['id']

        # should be one more now
        response = self.get_check_200('user-list')
        assert response.data['count'] == no_of_users + 1

        response = self.get_check_200('user-detail', pk=new_id)
        assert response.data['email'] == initial_mail
        # password should not be returned
        assert 'password' not in response.data
        self.assertURLsEqual(response.data['groups'], [group])
        self.assertURLsEqual(response.data['casestudies'], [lodz])

        new_mail = 'new@mail.de'
        data = {'email': new_mail, }
        response = self.patch('user-detail', pk=new_id, data=data)
        self.response_200()
        assert response.data['email'] == new_mail

        new_password = 'MyNewPassword'
        data = {'password': new_password, }
        response = self.patch('user-detail', pk=new_id, data=data)
        self.response_200()

    def test_permission(self):
        open_country = self.casestudy
        forbidden_country = CaseStudyFactory(name='ForbiddenCountry')
        # add anonymus user to casestudy1
        UserInCasestudy.objects.create(user=self.anonymus_user,
                                       casestudy=open_country)

        # try to access without login (anomymus user should be used by default)
        url = self.reverse('casestudy-detail', pk=open_country.pk)
        self.get_check_200(url)
        # second should be denied
        url = self.reverse('casestudy-detail', pk=forbidden_country.pk)
        response = self.get(url)

        # try access to casestudies with beeing logged in as anonymus user
        self.client.force_login(self.anonymus_user.user)
        # first casestudy should work
        url = self.reverse('casestudy-detail', pk=open_country.pk)
        self.get_check_200(url)
        # second should be denied
        url = self.reverse('casestudy-detail', pk=forbidden_country.pk)
        response = self.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # grant access
        anonymus_in_forbidden_country = UserInCasestudy.objects.create(
            user=self.anonymus_user,
            casestudy=forbidden_country)

        # should work now
        self.get_check_200(url)

        self.client.logout()
        # should still work
        self.get_check_200(url)

        # remove access
        anonymus_in_forbidden_country.delete()
        # should be denied now
        url = self.reverse('casestudy-detail', pk=forbidden_country.pk)
        response = self.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN


class CasestudyTest(BasicModelPermissionTest, APITestCase):

    url_key = "casestudy"
    url_pks = dict()
    url_pk = dict(pk=1)
    post_data = dict(name='posttestname')
    put_data = {'name': 'puttestname', }
    patch_data = dict(name='patchtestname')

    def test_post(self):
        url = self.url_key + '-list'
        # post
        response = self.post(url, **self.url_pks, data=self.post_data)
        for key in self.post_data:
            if key not in response.data.keys() or key in self.do_not_check:
                continue
            assert response.data[key] == self.post_data[key]

        # get
        new_id = response.data['id']
        url = self.url_key + '-detail'

        # casestudy is new -> noone may access it
        response = self.get(url, pk=new_id, **self.url_pks)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # grant access to new casestudy
        casestudy = CaseStudy.objects.get(id=new_id)
        casestudy.userincasestudy_set.add(self.uic)
        response = self.get_check_200(url, pk=new_id, **self.url_pks)

    def setUp(self):
        super().setUp()
        self.obj = self.kic.casestudy

    def test_session(self):
        casestudy_name = self.obj.name

        # at the beginning, no casestudy is selected
        casestudy = self.client.session.get('casestudy', None)
        assert casestudy is None

        # selecting a casestudy by posting to /login/session/
        url = '/login/session/'
        self.post(url, data={'casestudy': casestudy_name, })
        casestudy = self.client.session.get('casestudy', None)
        assert casestudy == casestudy_name

        # getting the selected casestudy
        response = self.get_check_200(url)
        assert response.json().get('casestudy', None) == casestudy_name


class UserInCasestudyTest(BasicModelPermissionTest, APITestCase):

    casestudy = 17
    user = 20

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url_key = "userincasestudy"
        cls.url_pks = dict(casestudy_pk=cls.casestudy)
        cls.url_pk = dict(pk=cls.user)
        cls.post_data = dict(role="role for testing")
        cls.put_data = dict(role="role for testing", user=cls.user)
        cls.patch_data = dict(role="role for testing")

    def setUp(self):
        super().setUp()
        self.obj = self.uic

    def test_delete(self):
        kwargs = {**self.url_pks, 'pk': self.obj.pk, }
        url = self.url_key + '-detail'
        response = self.get_check_200(url, **kwargs)

        # list all users in the casestudy
        response = self.get_check_200('userincasestudy-list', **self.url_pks)

        # delete is not allowed
        response = self.delete(url, **kwargs)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

        # delete manually
        uic = UserInCasestudy.objects.get(pk=self.obj.pk)
        uic.delete()
        response = self.get('userincasestudy-list', **self.url_pks)

        # after removing user
        # the casestudy is not permitted to access for this user any more
        assert response.status_code == status.HTTP_403_FORBIDDEN
        self.response_403()

    @unittest.skip('no Post possible')
    def test_post(self):
        """no Post"""

    @unittest.skip('no Post possible')
    def test_post_permission(self):
        """no Post"""

    @unittest.skip('no Delete possible')
    def test_delete_permission(self):
        """no Delete"""

    @unittest.skip('not shure what is checked here')
    def test_filter_fields(self):
        """Test the filter fields request parameters"""
        kwargs = {**self.url_pks, 'pk': self.obj.pk, }
        url = self.url_key + '-detail'

        fields = ['user', 'role']
        data = {'field': fields}
        response = self.get_check_200(url, data=data, **kwargs)
        self.assertSetEqual(set(response.data.keys()), set(fields))

        # test fields of a list
        # create a second user
        casestudy = CaseStudy.objects.get(pk=self.casestudy)
        uic2 = UserInCasestudyFactory(casestudy=casestudy)
        response = self.get_check_200('userincasestudy-list',
                                      data=data,
                                      casestudy_pk=self.casestudy)
        for row in response.data:
            self.assertSetEqual(set(row.keys()), set(fields))
