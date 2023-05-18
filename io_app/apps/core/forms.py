from django import forms
from django.core.exceptions import ValidationError
from io_app.consts import MessagesConsts, ProcessesConsts, MediaConsts
from io_app.apps.storage_manager import models


class StartFileProcessForm(forms.Form):
    file_name = forms.ChoiceField(label="", widget=forms.Select(attrs={
        "class": "form-select",
    }))

    process_type_name = forms.ChoiceField(label="", widget=forms.Select(attrs={
        "class": "form-select",
    }), choices=[(process_name, process_name) for process_name in ProcessesConsts.PROCESSES_FOR_FILES_NAMES.values()])

    template_name = "components/form.html"

    def clean_file_name(self):
        data = self.cleaned_data["file_name"]
        file = models.File.objects.filter(owner=self.user, name=data).first()

        if not file:
            raise ValidationError(MessagesConsts.FILE_DOESNT_EXIST)

        return data

    def clean_process_type_name(self):
        data = self.cleaned_data["process_type_name"]

        if data not in ProcessesConsts.PROCESSES_FOR_FILES_NAMES.values():
            raise ValidationError(MessagesConsts.PROCESS_DOESNT_EXIST)

        return data
