from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url
from datetime import datetime
from io_app.consts import MediaConsts
from io_app.utils import files_utils


class Directory(models.Model):
    name = models.CharField(max_length=200, unique=False, null=False)
    uuid = models.CharField(max_length=32, unique=True, null=False, default=files_utils.generate_uuid)

    creation_date = models.DateTimeField(unique=False, null=False, default=datetime.utcnow)

    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="directories")
    shared_to_users = models.ManyToManyField(get_user_model(), related_name="shared_directories", blank=True)

    def __str__(self):
        return self.uuid

    def get_size(self):
        return sum([file.size for file in self.files.all()])

    def get_size_in_mb(self):
        return round((self.get_size() / MediaConsts.BYTES_IN_MB), 2)

    def get_files_count(self):
        return len(self.files.all())


class File(models.Model):
    name = models.CharField(max_length=200, unique=False, null=False)
    uuid = models.CharField(max_length=32, unique=True, null=False)

    extension = models.CharField(max_length=10, unique=False, null=False)
    size = models.IntegerField(unique=False, null=False)

    upload_date = models.DateTimeField(unique=False, null=False, default=datetime.utcnow)

    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="files")
    directory = models.ForeignKey(Directory, on_delete=models.CASCADE, related_name="files", blank=True, null=True)

    accessible_via_link = models.BooleanField(default=False)

    def __str__(self):
        return self.uuid

    def get_file_size_in_mb(self):
        return round((self.size / MediaConsts.BYTES_IN_MB), 2)

    def get_directory_name(self):
        return self.directory.name if self.directory else "root"

    def get_directory_url(self):
        url = resolve_url("core:directory_content", directory_uuid=self.directory.uuid) \
            if self.get_directory_name() != "root" else resolve_url("core:home")

        return url

    def check_if_shared_to_user(self, user):
        shared = False

        if self.directory and user in self.directory.shared_to_users.all():
            shared = True

        return shared

    def can_be_previewed(self):
        can_be_previewed = False

        if self.extension in MediaConsts.CAN_BE_PREVIEWED_EXTENSIONS:
            can_be_previewed = True

        return can_be_previewed
