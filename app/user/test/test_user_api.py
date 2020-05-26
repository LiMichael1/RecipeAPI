from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token') 


def create_user(**param):
    return get_user_model().objects.create_user(**param)


class PublicUserApiTests(TestCase):
    """Test the user API (public)"""

    def setup(self):
        # don't have to create client for every test function
        self.client = APIClient()

    def test_create_valid_user_successful(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'test@gmail.com',
            'password': 'testpass',
            'name': 'test name'
        }
        # Post request to create a new user
        res = self.client.post(CREATE_USER_URL, payload)

        # is the response a 201 Created Response?
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # is object actually created?
        # object is returned after post request in "res"
        user = get_user_model().objects.get(**res.data)
        # Check if password from payload is correctly entered
        self.assertTrue(user.check_password(payload['password']))
        # check pass is not returned in request
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a user that already exists fails"""
        payload = {'email': 'test@gmail.com', 'password': 'testpass', 'name': 'Test'}
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        # 400 request when creating user that already exists
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password must be more than 5 characters"""
        payload = {'email': 'test@gmail.com', 'password': 'pw', 'name': 'Test'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)

    """TOKEN TESTING"""

    # Able to create token for a user? 
    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {'email': 'test@gmail.com', 'password': 'testpass'}
        
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        # a Token has been returned in the post response
        self.assertIn('token', res.data)
        # is 200 OK response?
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    # Wrong password or username?
    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email='test@gmail.com', password='testpass')
        # Incorrect password entered
        payload = {'email': 'test@gmail.com', 'password': 'wrong'} 
        res = self.client.post(TOKEN_URL, payload)

        # No Token and 400 BAD REQUEST returned
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # Don't create token when the user doesn't exist
    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exist"""
        payload = {'email': 'test@gmail.com', 'password': 'testpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # Don't create token when user is missing email or password
    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    