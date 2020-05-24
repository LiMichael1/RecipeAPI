""" Test helper functions can create users """
from django.test import TestCase
# User Authenticatoin from Django
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """ Test creating a new user with an email is successful"""
        email = 'test@gmail.com'
        password = 'Testpass123'

        # creates a user
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        # test if user was created successfully
        self.assertEqual(user.email, email)
        # Returns true if password is correct
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@GMAIL.com'
        user = get_user_model().objects.create_user(email, 'test123')

        # check if lower case is the same as upper case
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@gmail.com',
            'test123'
        )

        # user.is_superuser already created in the migrations
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
