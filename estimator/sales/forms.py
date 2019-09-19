import json

from django import forms
from .models import Sale, MaterialSaleRelation, DolarPrice
from raw_materials.models import RawMaterial


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

    def save(self, commit=True):
        """Metodo de guardar Una Compra"""
        # print('Intento de guardar')
        instance = super(SaleForm, self).save(commit=False)
        data = self.cleaned_data
        print(data)
        loaded_json = json.loads(data['raw_materials_json'])
        for x in loaded_json:
            print(x)

        if commit:
            print('Intento de guardar')
            pass
            # instance.save()
            # self.save_m2m()
        return instance
