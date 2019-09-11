from django import forms
from .models import Provider, RawMaterial


class ProviderForm(forms.ModelForm):
    """ Formulario de los proveedores """

    class Meta:
        model = Provider
        fields = ("name", "company")


class RawMaterialForm(forms.ModelForm):
    """Formulario de la materia prima"""

    years_to_expire = forms.IntegerField(, required=False)

    months_to_expire = forms.IntegerField(, required=False)

    days_to_expire = forms.IntegerField(, required=False)

    class Meta:
        model = RawMaterial
        fields = (
            "name",
            "company",
            "providers",
            "measurement_unit",
            "can_expire",
            "time_to_expire",
            "is_imported",
        )
