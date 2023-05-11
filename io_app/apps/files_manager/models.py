from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime


class File(models.Model):
    name = models.CharField(max_length=200, unique=False, null=False)
    uuid = models.CharField(max_length=32, unique=True, null=False)

    extension = models.CharField(max_length=10, unique=False, null=False)
    size = models.IntegerField(unique=False, null=False)

    upload_date = models.DateTimeField(unique=False, null=False, default=datetime.utcnow)

    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="files")

    def __str__(self):
        return self.uuid

    def get_file_size_in_mb(self):
        return round((self.size / 1048576), 2)
