from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model


@override_settings(
    CACHES={
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "unique-snowflake",
        }
    })
class TestViews(TestCase):
    def setUp(self):
        self.username = "user"
        self.password = "12345678"

        self.client = Client()

        get_user_model().objects.create_user(username=self.username, password=self.password)

    def test_home_as_non_auth(self):
        path = reverse("core:home")
        response = self.client.get(path)

        self.assertEqual(response.status_code, 302)

    def test_home_as_auth(self):
        logged_in = self.client.login(username=self.username, password=self.password)

        self.assertIs(logged_in, True)

        path = reverse("core:home")
        response = self.client.get(path)

        self.assertEqual(response.status_code, 200)