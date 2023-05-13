from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
from io_app.consts import SizesConsts
from io_app.utils import files_utils


class Directory(models.Model):
    name = models.CharField(max_length=200, unique=False, null=False)
    uuid = models.CharField(max_length=32, unique=True, null=False, default=files_utils.generate_uuid)

    creation_date = models.DateTimeField(unique=False, null=False, default=datetime.utcnow)

    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="directories")

    def __str__(self):
        return self.uuid

    def get_size(self):
        return sum([file.size for file in self.files.all()])

    def get_size_in_mb(self):
        return round((self.get_size() / SizesConsts.BYTES_IN_MB), 2)

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

    def __str__(self):
        return self.uuid

    def get_file_size_in_mb(self):
        return round((self.size / SizesConsts.BYTES_IN_MB), 2)

    def get_directory_name(self):
        return self.directory.name if self.directory else "root"
