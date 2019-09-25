import json

from django import forms
from .models import Sale, MaterialSaleRelation, DolarPrice
from raw_materials.models import RawMaterial, Provider
from django.utils.translation import gettext as _


class SaleForm(forms.ModelForm):

    dollar_price = forms.FloatField(
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
        self.creator_user = kwargs.pop('user')

        try:
            self.editing = kwargs.pop('editing')
        except Exception:
            self.editing = False

        super(SaleForm, self).__init__(*args, **kwargs)
        try:
            self.fields['dollar_price'].initial = kwargs['instance'].dollar_price.dollar_price
        except Exception:
            try:
                self.fields['dollar_price'].initial = DolarPrice.objects.latest('created').dollar_price
            except Exception:
                self.fields['dollar_price'].initial = 1
        if self.creator_user.is_superuser:
            company = self.creator_user.company
        else:
            company = self.creator_user.companyuser.company

        self.fields['raw_materials'].queryset = RawMaterial.objects.filter(
            company=company.pk,
        )

    class Meta:
        model = Sale
        fields = (
            "total_cost_dollar",
            "total_cost_local",
            "raw_materials"
        )

    # Logica de limpieza de datos
    def clean(self):
        """Verificando que las materias primas tengan un formato correcto"""
        data = super().clean()
        raw_materials_json = json.loads(data['raw_materials_json'])
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

            if float(val['cost_dollar']) < 0:
                errors.append(forms.ValidationError(
                    _('Costo en dolar no valido: %(value)s'),
                    code='invalid',
                    params={
                        'value': val['cost_dollar'],
                    },
                ))

            if float(val['cost_local']) < 0:
                errors.append(forms.ValidationError(
                    _('Costo local no valido: %(value)s'),
                    code='invalid',
                    params={
                        'value': val['cost_local'],
                    },
                ))
        if errors:
            raise forms.ValidationError(errors)

        return data

    def save(self, commit=True):
        """Metodo de guardar Una Compra"""
        instance = super(SaleForm, self).save(commit=False)
        data = self.cleaned_data
        dollar_price = DolarPrice(dollar_price=data.pop('dollar_price'))

        raw_materials_json = json.loads(data['raw_materials_json'])
        materials_sale_relation = []
        for raw_material in data['raw_materials']:
            temp = next(
                    (item for item in raw_materials_json if item["raw_material_pk"] == raw_material.pk),
                    None
                )
            if not self.editing:
                temp.pop('pk')

            # temp.pop('bought_in_dollars')
            temp.pop('name')
            temp.pop('measurement_unit')
            temp.pop('raw_material_pk')
            temp.pop('providers_list')

            provider_pk = temp.pop('provider')
            temp['raw_material'] = raw_material
            temp['provider'] = Provider.objects.get(pk=provider_pk)
            materials_sale_relation.append(
                MaterialSaleRelation(**temp)
            )

        if self.creator_user.is_superuser:
            instance.company = self.creator_user.company
        else:
            instance.company_user = self.creator_user.companyuser

        if commit:
            dollar_price.save()
            instance.dollar_price = dollar_price
            instance.save()

            for el in materials_sale_relation:
                # Saving the many to many
                el.sale = instance
                el.save()
        return instance
