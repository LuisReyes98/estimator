from django import forms
from django.utils.translation import gettext as _


class SelectPredictionForm(forms.Form):

    date = forms.DateField( # datetime.date
        label=_("Fecha de prediccion"),
        required=True
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')

        super(SelectPredictionForm, self).__init__(*args, **kwargs)

    class Meta:
        pass

    def clean(self):
        data = super().clean()
        # print(type(data['date']))
        self.request.session['prediction_date'] = data['date'].strftime("%Y-%m-%d")

        return data

    def save(self):
        pass
