from django.test import TestCase, Client, override_settings
from django.contrib.auth import get_user_model
from django.contrib import auth
from io_app.apps.authenticate import forms


@override_settings(
    CACHES={
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "unique-snowflake",
        }
    })
class TestForms(TestCase):
    def setUp(self):
        self.username = "user"
        self.password = "12345678"

        self.client = Client()

        get_user_model().objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)

        self.user = auth.get_user(self.client)

    def test_login_form_valid_data(self):
        form = forms.LoginForm(data={
            "username": self.username,
            "password": self.password
        })

        form.user = self.user

        self.assertTrue(form.is_valid())

    def test_login_form_empty_data(self):
        form = forms.LoginForm(data={
            "username": "",
            "password": ""
        })

        form.user = self.user

        self.assertFalse(form.is_valid())

    def test_login_form_invalid_data(self):
        form = forms.LoginForm(data={
            "username": self.username,
            "password": "invalid_pass"
        })

        form.user = self.user

        self.assertTrue(form.is_valid())
