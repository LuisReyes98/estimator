""" Formularios de los usuarios """

from django.forms import ModelForm
from users.models import Company
from users.models import CompanyUser


class RegisterCompanyForm(ModelForm):

    class Meta:
        model = Company
        fields = ("company_name",)
