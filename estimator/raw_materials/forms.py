from django import forms
from .models import Provider


class ProviderForm(forms.ModelForm):
    """ Formulario de los proveedores """

    class Meta:
        model = Provider
        fields = ("name", "company")
