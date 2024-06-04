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
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

