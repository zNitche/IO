from django.test import TestCase, Client, override_settings
from django.contrib.auth import get_user_model


@override_settings(
    CACHES={
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "unique-snowflake",
        }
    })
class TestModels(TestCase):
    def setUp(self):
        self.username = "user"
        self.password = "12345678"

        self.client = Client()

        get_user_model().objects.create_user(username=self.username, password=self.password)

    def test_new_user_creation(self):
        get_user_model().objects.create_user(username="test_user", password="1234567890")
        user = get_user_model().objects.filter(username="test_user").first()

        self.assertIsNot(user, None)

    def test_existing_user(self):
        user = get_user_model().objects.filter(username=self.username).first()

        self.assertIsNot(user, None)
