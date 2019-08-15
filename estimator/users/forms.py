""" Formularios de los usuarios """

from django import forms
from django.utils.translation import ugettext_lazy as translate
from users.models import AppUser, Company, CompanyUser


class CreateCompanyForm(forms.ModelForm):
    password_confirmation = forms.CharField(
        label=translate('Password confirmation'),
        max_length=70,
        widget=forms.PasswordInput(),
        required=True,
    )
    company_name = forms.CharField(
        label="Nombre de la Compañia",
        max_length=90,
        widget=forms.TextInput(),
        required=True,
    )

    class Meta:
        model = AppUser
        fields = (
            "email",
            "first_name",
            "last_name",
            "password",
        )

    # Logica de guardado y limpieza de datos

