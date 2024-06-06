from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.test import TestCase
from django.utils.text import slugify
from rest_framework_simplejwt.tokens import RefreshToken
from api.models import StreamingPlatform, WatchList
from api.factories import StreamingPlatformFactory, WatchListFactory


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


class WatchListBaseTestCase(APITestCase):
    def setUp(self):
        self.platform = StreamingPlatform.objects.create(
            streamer="Netflix",
            about="Popular streaming",
            url="https://www.netflix.com",
        )

        self.watchlist_data = {
            "title": "Invasion",
            "description": "science fiction",
            "platform": self.platform.id,
            "active": True,
            "average_rating": 4.5,
            "number_rating": 80,
        }

        self.invalid_watchlist_data = {
            "title": "",
            "description": "Top suspense. No title",
            "platform": self.platform.id,
            "active": False,
            "average_rating": 2.0,
            "number_rating": 3
        }

        self.admin_user = User.objects.create_superuser('admin', '<EMAIL>', '<PASSWORD>')
        self.client = APIClient()

        refresh_token = RefreshToken.for_user(self.admin_user)
        self.access_token = str(refresh_token.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer' + self.access_token)


class CreateWatchListTestCase(WatchListBaseTestCase):
    def test_create_watch_list(self):
        response = self.client.post(reverse('watch_list'), self.watchlist_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WatchList.objects.count(), 1)
        self.assertIn('Invasion', response.json().get('title'))

    def test_create_watch_list_invalid(self):
        response = self.client.post(reverse('watch_list'), self.invalid_watchlist_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(WatchList.objects.count(), 0)


class RetrieveWatchListTestCase(WatchListBaseTestCase):
    def test_retrieve_watch_list(self):
        watch_list = WatchListFactory(platform=self.platform)
        response = self.client.get(reverse('watch_list'))
        self.assertIsInstance(watch_list, WatchList)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)


class WatchListModelTestCase(TestCase):
    def setUp(self):
        self.streaming_platform = StreamingPlatformFactory()
        self.watchlist_data = WatchListFactory()

    def test_create_watchlist(self):
        watchlist = WatchListFactory(platform=self.streaming_platform)
        self.assertIsInstance(watchlist, WatchList)
        self.assertEqual(watchlist.platform, self.streaming_platform)
        self.assertIsNotNone(watchlist.created_at)

    def test_slug_create(self):
        watchlist = WatchListFactory(platform=self.streaming_platform)
        self.assertEqual(watchlist.slug, slugify(watchlist.title))

    def test_blank_slug(self):
        watchlist = WatchListFactory(platform=self.streaming_platform, slug="")
        self.assertEqual(watchlist.slug, slugify(watchlist.title))

    def test_update_watchlist(self):
        watchlist = WatchListFactory(platform=self.streaming_platform)
        watchlist.title = "updated title"
        watchlist.save()
        self.assertEqual(watchlist.title, "updated title")
        self.assertEqual(watchlist.slug, slugify("updated title"))

    def test_watchlist_associated_with_platform(self):
        watchlist = WatchListFactory(platform=self.streaming_platform)
        self.assertEqual(watchlist.platform.streamer, self.streaming_platform.streamer)
