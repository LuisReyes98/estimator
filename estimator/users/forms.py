""" Formularios de los usuarios """

from django import forms
from users.models import Company, CompanyUser, AppUser


class AppUserForm(forms.ModelForm):
    password_confirmation = forms.CharField(
        max_length=70,
        widget=forms.PasswordInput()
    )

    class Meta:
        model = AppUser


class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ("company_name", "user")


class CompanyUserForm(forms.ModelForm):

    class Meta:
        model = CompanyUser
        fields = ("",)
