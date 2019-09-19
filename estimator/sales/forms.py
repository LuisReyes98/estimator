import json

from django import forms
from .models import Sale, MaterialSaleRelation, DolarPrice
from raw_materials.models import RawMaterial
from django.utils.translation import gettext as _


class SaleForm(forms.ModelForm):

    dolar_price = forms.FloatField(
        label="Precio del dolar en moneda local",
        min_value=0,
        required=True,
    )

    raw_materials_json = forms.CharField(
        label="Materias Primas",
        required=True
    )

    manual_costs = forms.BooleanField(
        label="Costos Finales manuales",
        required=False
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(SaleForm, self).__init__(*args, **kwargs)
        try:
            self.fields['dolar_price'].initial = DolarPrice.objects.latest('created').dollar_price
        except Exception:
            self.fields['dolar_price'].initial = 1

        self.fields['raw_materials'].queryset = RawMaterial.objects.filter(
            company=user.company.pk,
        )

    class Meta:
        model = Sale
        fields = (
            "total_cost_dollar",
            "total_cost_local",
            "company",
            "company_user",
            "raw_materials"
        )

    # Logica de limpieza de datos
    def clean(self):
        """Verificando que las materias primas tengan un formato correcto"""
        data = super().clean()
        raw_materials_json = json.loads(data['raw_materials_json'])
        # print(data)
        errors = []

        for val in raw_materials_json:
            if int(val['amount']) < 1:
                errors.append(forms.ValidationError(
                    _('Cantidad no valida: %(value)s'),
                    code='invalid',
                    params={
                        'value': val['amount'],
                    },
                ))

            if float(val['dollar_cost']) < 0:
                errors.append(forms.ValidationError(
                    _('Costo en dolar no valido: %(value)s'),
                    code='invalid',
                    params={
                        'value': val['dollar_cost'],
                    },
                ))

            if float(val['local_cost']) < 0:
                errors.append(forms.ValidationError(
                    _('Costo local no valido: %(value)s'),
                    code='invalid',
                    params={
                        'value': val['local_cost'],
                    },
                ))
        if errors:
            raise forms.ValidationError(errors)

        return data

    def save(self, commit=True):
        """Metodo de guardar Una Compra"""
        instance = super(SaleForm, self).save(commit=False)
        data = self.cleaned_data
        # print(data)
        # raw_materials_json = json.loads(data['raw_materials_json'])
        # for x in raw_materials_json:
        #     print(x)

        if commit:
            print('Intento de guardar')
            pass
            # instance.save()
            # self.save_m2m()
        return instance
