import json

from django import forms
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.translation import gettext as _

from raw_materials.models import RawMaterial
from sales.models import MaterialSaleRelation
from datetime import date, datetime

class SelectPredictionForm(forms.Form):

    date = forms.DateField(  # datetime.date
        label=_("Fecha de prediccion"),
        required=True
    )

    raw_materials = forms.ModelMultipleChoiceField(
        label=_("Escoge las materias primas a predecir"),
        queryset=None,
        required=True
    )

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company')
        self.request = kwargs.pop('request')
        super(SelectPredictionForm, self).__init__(*args, **kwargs)

        self.fields['raw_materials'].queryset = RawMaterial.objects.filter(
            company=company.pk,
        )

    def clean(self):
        errors = []
        data = super(SelectPredictionForm, self).clean()
        date_string_error = data['date'].strftime("%m/%d/%Y")
        date_string = data['date'].strftime("%Y-%m-%d")

        if data['date'] < datetime.now().date():
            errors.append(forms.ValidationError(
                _('Error de fecha se escogio la fecha <b>%(value)s</b>, la cual es del pasado.'),
                code='invalid',
                params={
                    'value': date_string_error,
                },
            ))

        for material in data['raw_materials']:
            sales_relation_count = MaterialSaleRelation.objects.filter(
                raw_material=material.pk
            ).count()

            if sales_relation_count == 0:
                errors.append(forms.ValidationError(
                    _('La materia prima <b>%(value)s</b> no ha formado parte de ninguna compra.'),
                    code='invalid',
                    params={
                        'value': material.name,
                    },
                ))
            elif sales_relation_count == 1:
                errors.append(forms.ValidationError(
                    _('La materia prima <b>%(value)s</b> se ha comprado una unica vez, siendo no apta para predicciones.'),
                    code='invalid',
                    params={
                        'value': material.name,
                    },
                ))


        if errors:
            raise forms.ValidationError(errors)

        self.request.session['prediction_date'] = date_string
        self.request.session['prediction_raw_materials'] = json.dumps(
            list(
                data['raw_materials'].values(
                    'name',
                    'pk',
                )
            ),
            cls=DjangoJSONEncoder
        )

        return data

    class Meta:
        pass
