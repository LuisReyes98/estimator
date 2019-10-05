from django import forms
from django.utils.translation import gettext as _
from raw_materials.models import RawMaterial


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
        super(SelectPredictionForm, self).__init__(*args, **kwargs)

        self.fields['raw_materials'].queryset = RawMaterial.objects.filter(
            company=company.pk,
        )


    class Meta:
        pass

    # def clean(self):
    #     data = super().clean()
    #     # print(type(data['date']))
    #     # self.request.session['prediction_date'] = data['date'].strftime("%Y-%m-%d")

    #     return data

    # def save(self):
    #     pass
