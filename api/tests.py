from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken

from api import serializers
from api.models import StreamingPlatform


class StreamPlatformTestCase(APITestCase):

    def setUp(self):
        self.streamer_data = {
            "streamer": "Netflix",
            "about": "Popular streaming platform",
            "url": "https://www.netflix.com",
        }

        self.invalid_streamer_data = {
            "about": "Popular streaming platform",
            "url": "https://www.netflix.com",
            "streamer": "",

        }

        self.admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')
        self.client = APIClient()

        refresh = RefreshToken.for_user(self.admin_user)
        self.access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def test_create_streaming_platform(self):
        response = self.client.post(reverse("streaming_channels_create"), self.streamer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(StreamingPlatform.objects.count(), 1)
        self.assertEqual(StreamingPlatform.objects.get().streamer, "Netflix")

    def test_create_invalid_streaming_platform(self):
        response = self.client.post(reverse("streaming_channels_create"), self.invalid_streamer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_streaming_platform(self):
        streaming_platform = StreamingPlatform.objects.create(**self.streamer_data)
        response = self.client.get(reverse("streaming_channels_detail", args=[streaming_platform.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['streamer'], 'Netflix')

    def test_update_streaming_platform(self):
        streaming_platform = StreamingPlatform.objects.create(**self.streamer_data)
        update_data = {
            "streamer": "Netflix 2.0",
            "about": "Popular streaming platform version 2.0",
            "url": "https://www.netflix-v2.com",
        }
        response = self.client.put(
            reverse('streaming_channels_detail',
                    args=[streaming_platform.id]), update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Netflix 2.0", response.data['streamer'])

    def test_delete_streaming_platform(self):
        streaming_platform = StreamingPlatform.objects.create(**self.streamer_data)
        response = self.client.delete(reverse("streaming_channels_detail", args=[streaming_platform.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(StreamingPlatform.objects.count(), 0)
