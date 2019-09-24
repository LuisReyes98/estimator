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
        label="Nombre de la Compañía",
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

    def __init__(self, *args, **kwargs):
        super(CreateCompanyForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['password'].widget = forms.PasswordInput()

    # Logica de limpieza de datos
    def clean(self):
        """Verificando que las contraseñas coinciden"""
        data = super().clean()
        # Debido a que se necesita acceder a dos datos
        password = data['password']
        password_confirmation = data['password_confirmation']

        if password != password_confirmation:
            raise forms.ValidationError('Contraseñas no coinciden')

        return data

    # Logica de guardado
    def save(self):
        """Crear usuario y compañia"""
        data = self.cleaned_data

        company_name = data.pop('company_name')

        data.pop('password_confirmation')

        data['is_superuser'] = True

        user = AppUser.objects.create_user(**data)
        user.save()

        company = Company(user=user, company_name=company_name)
        company.save()

class CreateCompanyUserForm (forms.ModelForm):

    password_confirmation = forms.CharField(
        label=translate('Password confirmation'),
        max_length=70,
        widget=forms.PasswordInput(),
        required=True,
    )

    company = forms.IntegerField(required=True)

    class Meta:
        model = AppUser
        fields = (
            "email",
            "first_name",
            "last_name",
            "password",
            "is_staff",
        )

    def __init__(self, *args, **kwargs):
        # self.creator_company = kwargs.pop('creator_company')

        super(CreateCompanyUserForm, self).__init__(*args, **kwargs)
        # print(self.creator_company)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['password'].widget = forms.PasswordInput()

    # Logica de limpieza de datos
    def clean(self):
        """Verificando que las contraseñas coinciden"""
        data = super().clean()
        # Debido a que se necesita acceder a dos datos
        password = data['password']
        password_confirmation = data['password_confirmation']

        if password != password_confirmation:
            raise forms.ValidationError('Contraseñas no coinciden')

        return data

    # Logica de guardado
    def save(self):
        """Crear usuario y compañia"""
        print("Guardando")

        data = self.cleaned_data

        data.pop('password_confirmation')
        company = data.pop('company')
        data['is_superuser'] = False
        #import pdb; pdb.set_trace()
        user = AppUser.objects.create_user(**data)
        user.save()
        company_user_temp = CompanyUser(user=user, company=Company.objects.get(pk=company))
        company_user_temp.save()
        # company = Company(user=user, company_name=company_name)
        # company.save()