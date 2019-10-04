import copy
import csv
import json
import os
from datetime import datetime

from django.core.files.base import ContentFile
from django import forms
from django.conf import settings
from django.core.files.storage import default_storage
from django.utils.translation import gettext as _

from raw_materials.models import Provider, RawMaterial

from .models import DolarPrice, MaterialSaleRelation, Sale, SaleFile


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

        self.fields['raw_materials'].queryset = RawMaterial.objects.filter(
            company=self.creator_user.safe_company.pk,
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
            if int(val['provider']) == 0:
                errors.append(forms.ValidationError(
                    _('Proveedor no valido'),
                    code='invalid',
                ))
        if errors:
            raise forms.ValidationError(errors)

        return data

    def get_array_dict_value(self, array, key_name, comparator):
        """en un vector de diccionarios retorna el primer diccionario
            que contenga el valor del campo key_name igual al comparator
        """
        my_array = [copy.copy(element) for element in array]
        for el in my_array:
            if el[key_name] == comparator:
                return el

    def save(self, commit=True):
        """Metodo de guardar Una Compra"""
        instance = super(SaleForm, self).save(commit=False)

        # import pdb; pdb.set_trace()
        # instance['date'] = datetime.now()

        data = self.cleaned_data
        # agregando nueva fecha
        instance.date = datetime.now()

        dollar_price = DolarPrice(
            dollar_price=data.pop('dollar_price'),
            date=datetime.now()
        )

        raw_materials_json = json.loads(data['raw_materials_json'])
        materials_sale_relation = []

        for raw_material in data['raw_materials']:
            """Por cada materia prima seleccionada"""

            data_to_save = self.get_array_dict_value(
                raw_materials_json,
                'raw_material_pk',
                raw_material.pk
            )

            data_to_save.pop('name')
            data_to_save.pop('measurement_unit')
            data_to_save.pop('raw_material_pk')
            data_to_save.pop('providers_list')

            provider_pk = data_to_save.pop('provider')
            data_to_save['raw_material'] = raw_material
            data_to_save['provider'] = Provider.objects.get(pk=provider_pk)

            primary_key = data_to_save.pop('pk')

            try:
                # Editando
                relation = MaterialSaleRelation.objects.get(pk=primary_key)
            except Exception:
                # Creando
                relation = MaterialSaleRelation(**data_to_save)
            else:
                # Continua la edicion
                relation.amount = data_to_save['amount']
                relation.cost_dollar = data_to_save['cost_dollar']
                relation.cost_local = data_to_save['cost_local']
                relation.bought_in_dollars = data_to_save['bought_in_dollars']
                relation.provider = data_to_save['provider']
            materials_sale_relation.append(
                relation
            )

        instance.company = self.creator_user.safe_company
        if not self.creator_user.is_superuser:
            instance.company_user = self.creator_user.companyuser

        if commit:
            dollar_price.save()
            instance.dollar_price = dollar_price
            instance.save()

            for el in materials_sale_relation:
                # Guardando mucho a muchos
                el.sale = instance
                el.save()

            self.save_m2m()
        return instance


class SaleFileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.creator_company = kwargs.pop('company')

        super(SaleFileForm, self).__init__(*args, **kwargs)

    class Meta:
        model = SaleFile
        fields = ("sale_upload",)

    def is_valid_csv_header(self, header):
        header_format = SaleFile.FILE_HEADER_FORMAT
        num_base_col = 4

        material_counter = 1
        # se chequean las primeras 3 columnas por separado de las demas
        for k in range(num_base_col):
            if header[k] != header_format[k]:
                print(header[k])
                return False

        for i in range(num_base_col, len(header), 6):
            for j in range(6):
                file_col = header[i + j]
                model_col = header_format[j+num_base_col][:-1]+str(material_counter)

                if file_col != model_col:
                    return False
            material_counter += 1

        return True

    def clean(self, *args, **kwargs):
        # Confirmando que sea un archivo csv
        cleaned_data = super(SaleFileForm, self).clean()
        try:
            cleaned_data['sale_upload']
        except KeyError:
            raise forms.ValidationError(
                _('El archivo es requerido'),
                code='invalid',
            )
        if not cleaned_data['sale_upload'].name.endswith('.csv'):
            raise forms.ValidationError(
                _('Debe ser un archivo en formato csv'),
                code='invalid',
            )
        readable_file = copy.copy(cleaned_data['sale_upload'])

        build_path = getattr(settings, 'MEDIA_ROOT')+'/tmp/'+readable_file.name

        csv.register_dialect(
            'semi_col',
            delimiter=';',
            quoting=csv.QUOTE_NONE
        )
        file_path = default_storage.save(build_path, ContentFile(readable_file.read()))

        reader = csv.reader(open(file_path, 'r'), 'semi_col')
        i = 0
        row_count = 0
        try:
            for row in reader:
                if i == 0:
                    header = row
                i += 1
                row_count += 1
        except csv.Error:
            raise forms.ValidationError(
                _('El archivo esta mal formulado o dañado'),
                code='invalid',
            )

        if row_count > 150:
            raise forms.ValidationError(
                _('El maximo permitido por archivo son 150 ventas (151 filas)'),
                code='invalid',
            )

        if not self.is_valid_csv_header(header):
            raise forms.ValidationError(
                _('El archivo no posee el formato correcto de las cabeceras'),
                code='invalid',
            )

        default_storage.delete(file_path)

        # Todo correcto retorna la data
        return cleaned_data

    def save(self, commit=True):
        instance = super(SaleFileForm, self).save(commit=False)
        instance.company = self.creator_company

        if commit:
            instance.save()
        return instance
