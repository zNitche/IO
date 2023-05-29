from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from io_app.apps.storage_manager import models
from io_app.utils import files_utils


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

        get_user_model().objects.create_user(username=self.username, password=self.password)

    def test_create_file(self):
        models.File.objects.create(name="test_file", uuid=files_utils.generate_uuid(), extension="txt", size=10,
                                   owner_id=1)
        file = models.File.objects.filter(name="test_file", owner_id=1).first()

        self.assertIsNot(file, None)

    def test_create_directory(self):
        models.Directory.objects.create(name="test_dir", uuid=files_utils.generate_uuid(), owner_id=1)
        directory = models.Directory.objects.filter(name="test_dir", owner_id=1).first()

        self.assertIsNot(directory, None)

    def test_add_file_to_directory(self):
        file = models.File.objects.create(name="test_file", uuid=files_utils.generate_uuid(), extension="txt", size=10, owner_id=1)
        directory = models.Directory.objects.create(name="test_dir", uuid=files_utils.generate_uuid(), owner_id=1)

        file.directory = directory

        self.assertIs(file.directory, directory)
