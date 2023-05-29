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

        get_user_model().objects.create_user(username=self.username, password=self.password, id=999)

    def test_storage_usage_as_anon(self):
        path = reverse("api:storage_usage")
        response = self.client.get(path)

        self.assertEqual(response.status_code, 302)

    def test_storage_usage_by_filetype_as_anon(self):
        path = reverse("api:storage_usage_by_filetype")
        response = self.client.get(path)

        self.assertEqual(response.status_code, 302)

    def test_running_processes_as_anon(self):
        path = reverse("api:running_processes")
        response = self.client.get(path)

        self.assertEqual(response.status_code, 302)

    def test_storage_usage_as_auth(self):
        logged_in = self.client.login(username=self.username, password=self.password)

        path = reverse("api:storage_usage")
        response = self.client.get(path)

        self.assertEqual(response.status_code, 200)
        self.assertIs(logged_in, True)

        response = self.client.get(path)

        self.assertJSONEqual(
            str(response.content, encoding="utf8"),
            {"free_space": 0,
             "used_space": 0}
        )

    def test_storage_usage_by_filetype_as_auth(self):
        logged_in = self.client.login(username=self.username, password=self.password)

        path = reverse("api:storage_usage_by_filetype")
        response = self.client.get(path)

        self.assertEqual(response.status_code, 200)
        self.assertIs(logged_in, True)

        response = self.client.get(path)

        self.assertJSONEqual(str(response.content, encoding="utf8"), {})
