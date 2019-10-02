# from django.shortcuts import render
from django.views.generic import FormView, TemplateView
from .forms import SelectPredictionForm
from django.urls import reverse_lazy

from sales.models import Sale
from raw_materials.models import RawMaterial
from datetime import datetime
import pytz
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso


class PredictionFormView(FormView):
    template_name = "predictions/select_prediction.html"
    success_url = reverse_lazy("predictions:result")
    form_class = SelectPredictionForm

    def get_form_kwargs(self):
        form_kwargs = super(PredictionFormView, self).get_form_kwargs()

        form_kwargs['request'] = self.request
        return form_kwargs


class PredictionResultView(TemplateView):
    template_name = "predictions/show_prediction.html"

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        sales = list(Sale.objects.filter(
            company=self.request.user.safe_company.pk,
        ).order_by('date'))

        # construyendo diccionario de datos a utilizar
        materials = [
            {
                **el.materials_sale_relation.values(
                    'cost_dollar',
                    'amount',
                    'raw_material'
                )[0],

                'dollar_price': el.dollar_price.dollar_price,
                'date': el.date.toordinal(),
            } for el in sales
        ]

        # print(materials[0])

        # print(sales[0].__dict__)
        xdf = pd.DataFrame(materials)
        print(xdf.head(1))

        xdf=xdf.dropna()

        # print(np.any(np.isnan(xdf)))
        print("hay valores nulos: ",np.any(np.isnan(xdf)))

        # import pdb; pdb.set_trace()
        # print(xdf)

        ydf = xdf['cost_dollar']
        ydf = ydf.dropna()

        xdf = xdf.drop('cost_dollar', axis=1)
        xdf=xdf.dropna()
        # xdf.dropna()

        print("Cabecera del df",xdf.head(1))

        print("Hay valores nulos: ",np.any(np.isnan(xdf)))
        xdf = xdf.reset_index()
        ydf = ydf.reset_index()

        # import pdb; pdb.set_trace()
        x_train, x_test, y_train, y_test = train_test_split(xdf,ydf,test_size=0.3)

        # chequeando columnas
        model = Lasso()  # usando el modelo Lasso
        # x_train.reset_index()
        # y_train.reset_index()
        # entrenado al modelo
        model.fit(x_train, y_train)
        # predecir los datos con los tests
        predicted = model.predict(x_test)
        # verificar tamaño
        print("Shape: ", predicted.shape)

        print("Score: ", model.score(x_test,y_test))
        """
            Primer score obtenido es 0.9997392317240795
            Lo mas probable es que no encontremos
            que el algoritmo esta en overfitting
        """
        # plt.hist(predicted)
        context['graph'] = plt.hist(predicted)
        print()


        print("Realizando prediccion")

        context['prediction_date'] = request.session['prediction_date']

        return self.render_to_response(context)
