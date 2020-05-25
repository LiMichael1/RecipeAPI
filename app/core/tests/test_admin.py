from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        """Set Up function runned before the tests"""
        self.client = Client()
        # Make sure user is logged into application
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@gmail.com',
            password='password123'
        )
        # helper function for admin to login during testing
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@gmail.com',
            password='password123',
            name='Test user full name'
        )

    def test_users_listed(self):
        """Test that users are listed on user page"""
        # generate url for list user page 
        url = reverse('admin:core_user_changelist')
        # GET request on URL using the Client
        res = self.client.get(url)

        # Checks for the name, email, and 200 Response Code
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    # Admin able to change user model
    def test_user_change_page(self):
        """Test that the user edit page works"""
        # url = /admin/core/user/{USER ID HERE}
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        # Check if Response is 200 OK
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """test that the create user page works"""
        # Classic Add Page
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        # Check if Response is 200 OK
        self.assertEqual(res.status_code, 200)