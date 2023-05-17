from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from io_app.consts import MessagesConsts
from io_app.apps.storage_manager import models


class AddDirectoryForm(forms.Form):
    directory_name = forms.CharField(label="", max_length=25, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "directory name"
    }))

    template_name = "components/form.html"

    def clean_directory_name(self):
        data = self.cleaned_data["directory_name"]
        directory = models.Directory.objects.filter(owner=self.user, name=data).first()

        if directory:
            raise ValidationError(MessagesConsts.DIRECTORY_EXISTS)

        return data


class ChangeDirectoryForm(forms.Form):
    directory_name = forms.ChoiceField(label="", widget=forms.Select(attrs={
        "class": "form-select",
    }))

    template_name = "components/form.html"

    def clean_directory_name(self):
        data = self.cleaned_data["directory_name"]

        if data != "root":
            directory = models.Directory.objects.filter(owner=self.user, name=data).first()

            if not directory:
                raise ValidationError(MessagesConsts.DIRECTORY_DOESNT_EXIST)

        return data


class UpdateDirectoryFilesForm(forms.Form):
    files = forms.MultipleChoiceField(label="", widget=forms.CheckboxSelectMultiple(attrs={
        "class": "checkboxes-wrapper",
    }))

    template_name = "components/form.html"

    def clean_files(self):
        data = self.cleaned_data["files"]

        for file_name in data:
            file = models.File.objects.filter(owner=self.user, name=file_name).first()

            if not file:
                raise ValidationError(MessagesConsts.FILE_DOESNT_EXIST)

        return data


class ShareDirectoryToUserForm(forms.Form):
    username = forms.CharField(label="", max_length=25, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "username"
    }))

    template_name = "components/form.html"

    def clean_username(self):
        data = self.cleaned_data["username"]
        user = get_user_model().objects.filter(username=data).first()

        if not user:
            raise ValidationError(MessagesConsts.USER_DOESNT_EXIST)

        if user and user == self.user:
            raise ValidationError(MessagesConsts.USER_DOESNT_EXIST)

        return data
