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

    # company = forms.IntegerField(required=True)

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
        self.creator_company = kwargs.pop('creator_company')
        super(CompanyUserForm, self).__init__(*args, **kwargs)
        # print(self.creator_company)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['password'].widget = forms.PasswordInput()

        try:
            self.fields['first_name'].initial = kwargs['instance'].user.first_name
            self.fields['last_name'].initial = kwargs['instance'].user.last_name
            self.fields['email'].initial = kwargs['instance'].user.email
            self.fields['is_staff'].initial = kwargs['instance'].user.is_staff
            pass
        except Exception:
            pass
        # import pdb; pdb.set_trace()

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
        # company_pk = data.pop('company')
        data['is_superuser'] = False

        if commit:
            user = AppUser.objects.create_user(**data)
            user.save()
            company_user = CompanyUser(
                user=user,
                company=self.creator_company
            )
            company_user.save()

        return instance

class CompanyUserFormFields (forms.ModelForm):
    """Formulario de edicion de un usuario miembro de una empresa"""

    # company = forms.IntegerField(required=True)

    class Meta:
        model = AppUser
        fields = (
            "email",
            "first_name",
            "last_name",
            "is_staff",
        )

    def __init__(self, *args, **kwargs):
        self.creator_company = kwargs.pop('creator_company')
        super(CompanyUserFormFields, self).__init__(*args, **kwargs)
        # print(self.creator_company)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

        self.fields['first_name'].initial = kwargs['instance'].user.first_name
        self.fields['last_name'].initial = kwargs['instance'].user.last_name
        self.fields['email'].initial = kwargs['instance'].user.email
        self.fields['is_staff'].initial = kwargs['instance'].user.is_staff
        # try:
        #     pass
        # except Exception:
        #     pass

        # import pdb; pdb.set_trace()


    def save(self, commit=True):
        """Logica de guardado guardando usuario"""
        instance = super(CompanyUserFormFields, self).save(commit=False)
        data = self.cleaned_data

        # company_pk = data.pop('company')
        data['is_superuser'] = False
        # import pdb; pdb.set_trace()
        if commit:
            user = instance.user
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.email = data['email']
            user.is_staff = data['is_staff']
            user.save()
            # company_user = instance
            instance.user = user
            instance.save()

        return instance

class CompanyUserFormPassword (forms.ModelForm):
    """Formulario de creacion de usuario miembro de una empresa"""

    password_confirmation = forms.CharField(
        label=translate('Password confirmation'),
        max_length=70,
        widget=forms.PasswordInput(),
        required=True,
    )

    # company = forms.IntegerField(required=True)

    class Meta:
        model = AppUser
        fields = (
            "password",
        )

    def __init__(self, *args, **kwargs):
        self.creator_company = kwargs.pop('creator_company')
        super(CompanyUserFormPassword, self).__init__(*args, **kwargs)
        # print(self.creator_company)
        self.fields['password'].widget = forms.PasswordInput()

        # import pdb; pdb.set_trace()

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
        instance = super(CompanyUserFormPassword, self).save(commit=False)
        data = self.cleaned_data

        data.pop('password_confirmation')
        # company_pk = data.pop('company')
        data['is_superuser'] = False

        if commit:
            user = instance.user
            user.set_password(data['password'])
            user.save()
            # company_user = instance
            instance.user = user
            instance.save()

        return instance