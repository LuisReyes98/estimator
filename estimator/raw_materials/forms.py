from django import forms
from .models import Provider, RawMaterial
from datetime import timedelta


class ProviderForm(forms.ModelForm):
    """ Formulario de los proveedores """

    class Meta:
        model = Provider
        fields = ("name", "company")


class RawMaterialForm(forms.ModelForm):
    """Formulario de la Materia Prima"""

    days_to_expire = forms.IntegerField(
        label="Días para expirar",
        min_value=0,
        max_value=999,
        required=False
    )

    months_to_expire = forms.IntegerField(
        label="Meses para expirar",
        min_value=0,
        max_value=999,
        required=False
    )

    years_to_expire = forms.IntegerField(
        label="Años para expirar",
        min_value=0,
        max_value=999,
        required=False
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(RawMaterialForm, self).__init__(*args, **kwargs)

        self.fields['days_to_expire'].initial = self.instance.days_to_expire
        self.fields['months_to_expire'].initial = self.instance.months_to_expire
        self.fields['years_to_expire'].initial = self.instance.years_to_expire

        self.fields['providers'].queryset = Provider.objects.filter(
            company=user.company.pk,
        )

    class Meta:
        model = RawMaterial
        fields = (
            "name",
            "company",
            "providers",
            "measurement_unit",
            "can_expire",
            "is_imported",
        )

    def times_to_timedelta(self, days, months, years):
        days = days if days is not None else 0
        months = months if months is not None else 0
        years = years if years is not None else 0

        return timedelta(
            days=(days + months * 30 + years * 365)
        )

    def save(self, commit=True):
        """Metodo de guardar materia prima """
        instance = super(RawMaterialForm, self).save(commit=False)
        data = self.cleaned_data

        expiration_time = {
            'days': data['days_to_expire'],
            'months': data['months_to_expire'],
            'years': data['years_to_expire']
        }
        instance.time_to_expire = self.times_to_timedelta(**expiration_time)

        if commit:
            instance.save()
            self.save_m2m()
        return instance
