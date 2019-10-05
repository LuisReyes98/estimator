from django import forms
from django.utils.translation import gettext as _
from raw_materials.models import RawMaterial
import json
from django.core.serializers.json import DjangoJSONEncoder


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
        data = super(SelectPredictionForm, self).clean()

        self.request.session['prediction_date'] = data['date'].strftime("%Y-%m-%d")

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
