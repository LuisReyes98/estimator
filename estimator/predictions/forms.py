from django import forms
from django.utils.translation import gettext as _
from sales.models import Sale
from raw_materials.models import RawMaterial

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso


class SelectPredictionForm(forms.Form):

    date = forms.DateField(
        label=_("Fecha de prediccion"),
        required=False
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')

        super(SelectPredictionForm, self).__init__(*args, **kwargs)

    class Meta:
        pass

    def clean(self):
        data = super().clean()

        sales = list(Sale.objects.filter(
            company=self.user.safe_company.pk,
        ).order_by('date'))

        # construyendo diccionario de datos a utilizar
        materials = [
            {
                **el.materials_sale_relation.values(
                    'cost_dollar',
                    'amount'
                )[0],
                'raw_material': RawMaterial.objects.get(
                    pk=el.materials_sale_relation.values(
                        'raw_material_id'
                    )[0]['raw_material_id']
                ).name,
                'dollar_price': el.dollar_price.dollar_price,
                'date': el.date
            } for el in sales
        ]

        # print(materials[0])

        # print(sales[0].__dict__)
        xdf = pd.DataFrame(materials)
        print(xdf)

        ydf = xdf['cost_dollar']

        xdf = xdf.drop('cost_dollar', axis = 1)

        x_train, x_test, y_train, y_test = train_test_split(
            xdf,
            ydf,
            test_size=0.3  # 30% de valores para test
        )

        # chequeando columnas
        print(xdf.head(1))
        model = Lasso()  # usando el modelo Lasso

        # entrenado al modelo
        model.fit(x_train, y_train)
        # predecir los datos con los tests
        predicted = model.predict(x_test)
        # verificar tamaño
        print(predicted.shape)

        print("Realizando prediccion")
        return data

    def save(self):
        pass
