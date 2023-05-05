from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="", max_length=25, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "username"
    }))

    password = forms.CharField(label="", max_length=32, widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "password"
    }))

    template_name = "components/form.html"
