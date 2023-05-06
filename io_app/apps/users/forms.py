from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from io_app.apps.users.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username",)
