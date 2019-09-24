from django import forms
from django.utils.translation import ugettext_lazy as translate
from users.models import AppUser, Company, CompanyUser


class CompanyUserForm (forms.ModelForm):
    """Formulario de creacion de usuario miembro de una empresa"""

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

        super(CompanyUserForm, self).__init__(*args, **kwargs)
        # print(self.creator_company)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['password'].widget = forms.PasswordInput()

    def clean(self):
        """Logica de limpieza de datos Verificando que las contraseñas coinciden"""
        data = super().clean()
        # Debido a que se necesita acceder a dos datos
        password = data['password']
        password_confirmation = data['password_confirmation']

        if password != password_confirmation:
            raise forms.ValidationError('Contraseñas no coinciden')

        return data

    def save(self, commit=True):
        """Logica de guardado guardando usuario"""
        instance = super(CompanyUserForm, self).save(commit=False)
        data = self.cleaned_data

        data.pop('password_confirmation')
        company_pk = data.pop('company')
        data['is_superuser'] = False

        if commit:
            user = AppUser.objects.create_user(**data)
            user.save()
            company_user = CompanyUser(
                user=user,
                company=Company.objects.get(pk=company_pk)
            )
            company_user.save()

        return instance
