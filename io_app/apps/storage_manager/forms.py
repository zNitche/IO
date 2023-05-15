from django import forms
from django.core.exceptions import ValidationError
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
