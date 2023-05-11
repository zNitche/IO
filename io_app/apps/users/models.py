from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from datetime import datetime
from io_app.apps.users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=25, unique=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=datetime.now)

    private_storage_space = models.IntegerField(default=0, null=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username

    def get_private_storage_space(self):
        return self.private_storage_space * 1048576
