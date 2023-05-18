from django import forms
from django.core.exceptions import ValidationError
from io_app.consts import MessagesConsts, MediaConsts
from io_app.apps.storage_manager import models


class StartArchiveExtractionProcessForm(forms.Form):
    file_name = forms.ChoiceField(label="", widget=forms.Select(attrs={
        "class": "form-select",
    }))

    template_name = "components/form.html"

    def clean_file_name(self):
        data = self.cleaned_data["file_name"]
        file = models.File.objects.filter(owner=self.user, name=data).first()

        if not file:
            raise ValidationError(MessagesConsts.FILE_DOESNT_EXIST)

        if file.extension not in MediaConsts.COMMON_ARCHIVE_EXTENSIONS:
            raise ValidationError(MessagesConsts.FILE_IS_NOT_ARCHIVE)

        return data
