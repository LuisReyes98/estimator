# from django.shortcuts import render
from django.views.generic import FormView, TemplateView
from .forms import SelectPredictionForm
from django.urls import reverse_lazy

from sales.models import Sale, DolarPrice
from raw_materials.models import RawMaterial
from datetime import datetime, date
import pytz
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import (
    train_test_split,
    cross_val_score,
    cross_validate
)
from sklearn.linear_model import Lasso, LassoCV, MultiTaskLasso

import io


class PredictionFormView(FormView):
    template_name = "predictions/select_prediction.html"
    success_url = reverse_lazy("predictions:result")
    form_class = SelectPredictionForm

    def get_form_kwargs(self):
        form_kwargs = super(PredictionFormView, self).get_form_kwargs()

        form_kwargs['company'] = self.request.user.safe_company
        return form_kwargs


class PredictionResultView(TemplateView):
    template_name = "predictions/show_prediction.html"

    def estimate_costs(self, date, xdf):
        print(xdf.head(1))

        

        # print(np.any(np.isnan(xdf)))
        print("hay valores nulos: ", np.any(np.isnan(xdf)))

        # import pdb; pdb.set_trace()
        # print(xdf)

        ydf = xdf['cost_dollar']
        ydf = ydf.dropna()

        xdf = xdf.drop('cost_dollar', axis=1)
        xdf = xdf.dropna()
        # xdf.dropna()

        print("Cabecera del df", xdf.head(1))

        print("Hay valores nulos: ", np.any(np.isnan(xdf)))
        xdf = xdf.reset_index()
        ydf = ydf.reset_index()

        # import pdb; pdb.set_trace()
        x_train, x_test, y_train, y_test = train_test_split(xdf, ydf, test_size=0.3)

        # chequeando columnas
        model = MultiTaskLasso()  # usando el modelo Lasso

        # results = cross_validate(model,xdf,ydf,return_train_score=True,cv=5)
        # print("cross validation: ",results)
        # entrenado al modelo

        model.fit(x_train, y_train)
        # predecir los datos con los tests

        predicted = model.predict(x_test)

        # verificar tamaño
        print("Shape: ", predicted.shape)

        print("Score: ", model.score(x_test, y_test))


        """
            Primer score obtenido es 0.9997392317240795
            Lo mas probable es que no encontremos
            que el algoritmo esta en overfitting
        """
        # plt.hist(predicted)
        plt.hist(predicted)
        my_stringIObytes = io.StringIO()
        plt.savefig(my_stringIObytes, format='svg')
        plt.close()

        return my_stringIObytes.getvalue()


    def get(self, request, *args, **kwargs):
        """
            Se recibira por atributo get
            Se recibira fecha
            Lista de materia prima a predecir
        """

        context = super().get_context_data(**kwargs)

        date = datetime.strptime(
            request.GET['date'],
            '%Y-%m-%d'
        )

        print(date)

        sales = list(Sale.objects.filter(
            company=self.request.user.safe_company.pk,
        ).exclude(
                date__isnull=True,
                raw_materials__isnull=True,
                dollar_price__isnull=True,
            ).order_by('date')
        )

        dolar_prices = list(
            DolarPrice.objects.exclude(
                date__isnull=True
            ).order_by('date')
        )
        dolar_prices = [
            {
                'date': el.date.toordinal(),
                'dollar_price': el.dollar_price
            } for el in dolar_prices
        ]

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
        xdf = xdf.dropna()


        #COst estimation
        graphic = self.estimate_costs(date, xdf)

        dolardf = pd.DataFrame(dolar_prices)

        dolardf = dolardf.dropna()
        # print(dolardf)

        # temperatura de precios materia prima
        sns.heatmap(xdf.corr())
        heatmapIO = io.StringIO()
        plt.savefig(heatmapIO, format='svg')
        plt.close()
        heatmapIO = heatmapIO.getvalue()

        sns.heatmap(dolardf.corr())
        dollarMap = io.StringIO()
        plt.savefig(dollarMap, format='svg')
        plt.close()
        dollarMap = dollarMap.getvalue()

        context['graphics'] = [
            graphic,
            heatmapIO,
            dollarMap
        ]

        # context['tempeture_graph'] = graphic

        print("Realizando prediccion")

        context['prediction_date'] = date

        return self.render_to_response(context)
