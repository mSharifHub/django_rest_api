from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User


class RegisterTestCase(APITestCase):
    def test_register_user(self):
        url = reverse('register')
        data = {
            'username': 'mock-user',
            'email': 'mock-user@mail.com',
            'password': '12345678910',
            'confirm_password': '12345678910'

        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'mock-user')

    def test_register_user_missing_fields(self):
        url = reverse('register')
        data = {
            'username': 'mock-user',
            'email': '',
            'password': '12345678910',
            'confirm_password': '12345678910',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AuthenticateTestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')

        self.user_data = {
            'username': 'mock-user',
            'email': 'mock-user@mail.com',
            'password': '<PASSWORD>',
            'confirm_password': '<PASSWORD>'
        }

        self.client.post(self.register_url, self.user_data, format='json')

    def test_login_user(self):
        data = {
            'username': 'mock-user',
            'password': '<PASSWORD>',
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.json())
        self.assertIn('refresh', response.json())

    def test_logout_user(self):
        login_data = {
            'username': 'mock-user',
            'password': '<PASSWORD>',
        }
        login_response = self.client.post(self.login_url, login_data, format='json')
        refresh_token = login_response.json()['refresh']

        logout_data = {
            'refresh': refresh_token,

        }

        logout_response = self.client.post(self.logout_url, logout_data, format='json')
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)
        self.assertIn("logged out successfully", logout_response.json()['message'])

    def test_invalid_user(self):
        data = {'username': 'mock-user', 'password': '<PASSD>'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_invalid_token(self):
        data = {
            'refresh': "invalid token"
        }
        response = self.client.post(self.logout_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
