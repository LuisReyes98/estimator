# from django.shortcuts import render
import io
import json
from datetime import date, datetime

import category_encoders as ce
import matplotlib
import numpy as np
import pandas as pd
import pytz
import seaborn as sns
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from matplotlib import pyplot as plt
from sklearn.linear_model import Lasso, LassoCV, MultiTaskLasso
from sklearn.model_selection import (cross_val_score, cross_validate,
                                     train_test_split)

from raw_materials.models import RawMaterial
from sales.models import DolarPrice, Sale

from .forms import SelectPredictionForm

matplotlib.use('Agg')




class PredictionFormView(FormView):
    template_name = "predictions/select_prediction.html"
    success_url = reverse_lazy("predictions:result")
    form_class = SelectPredictionForm

    def get_form_kwargs(self):
        form_kwargs = super(PredictionFormView, self).get_form_kwargs()

        form_kwargs['company'] = self.request.user.safe_company
        form_kwargs['request'] = self.request
        return form_kwargs


class PredictionResultView(TemplateView):
    template_name = "predictions/show_prediction.html"

    def estimate_costs(self, date, xdf):
        # print(np.any(np.isnan(xdf)))
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

        # predicted = model.predict(x_test)

        # verificar tamaño
        # print("Shape: ", predicted.shape)

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

    def build_dolar_dataframes(self):
        """ Retorna dataframe de los precios del dolar"""
        dolar_prices = list(
            DolarPrice.objects.filter(
                date__gte=date(2018, 8, 19)  # fecha despues del cambio de moneda
            ).exclude(
                date__isnull=True
            ).order_by('date')
        )
        dolar_prices = [
            {
                'date': el.date.toordinal(),
                'dollar_price': el.dollar_price
            } for el in dolar_prices
        ]
        xdf = pd.DataFrame(dolar_prices)
        xdf.dropna()

        return xdf

    def build_materials_dataframes(self, raw_materials):
        # contruyendo grupos de datos

        sales = list(Sale.objects.filter(
            company=self.request.user.safe_company.pk,
        ).exclude(
                date__isnull=True,
                raw_materials__isnull=True,
                dollar_price__isnull=True,
            ).order_by('date')
        )

        materials_dict = {}
        all_materials_array = []
        for material in raw_materials:
            materials_dict[material['pk']] = []
        # construyendo diccionario de datos a utilizar

        for sale in sales:
            for material in sale.materials_sale_relation:
                value = {
                            'cost_dollar': material.cost_dollar,
                            'amount': material.amount,
                            'raw_material': material.raw_material.pk,
                            'dollar_price': sale.dollar_price.dollar_price,
                            'date': sale.date.toordinal(),
                        }
                all_materials_array.append(value)
                if material.raw_material.pk in materials_dict:
                    materials_dict[material.raw_material.pk].append(
                        value
                    )
        # dataframe de todas las materias primas
        Xall_df = pd.DataFrame(all_materials_array)

        Xall_df = Xall_df.dropna()

        encoder = ce.BinaryEncoder(cols=['raw_material'])
        Xall_df = encoder.fit_transform(Xall_df)

        # diccionario de dataframes de las materias primas seleccionadas
        Xm_df_array = {}

        for key, value in materials_dict.items():
            df = pd.DataFrame(value)
            df = df.dropna()

            Xm_df_array[key] = df.drop('raw_material', 1)

        return (Xall_df, Xm_df_array)

    def train_model(self, model, dataframe, y_column_name):
        ydf = dataframe[y_column_name]
        ydf = ydf.dropna()

        xdf = dataframe.drop(y_column_name, axis=1)
        xdf = xdf.dropna()

        # xdf = xdf.reset_index()
        # ydf = ydf.reset_index()

        # import pdb; pdb.set_trace()
        x_train, x_test, y_train, y_test = train_test_split(xdf, ydf, test_size=0.35)

        # entrenado al modelo

        model.fit(x_train, y_train)
        # predecir los datos con los tests

        predicted = model.predict(x_test)

        # verificar tamaño

        # print("Predicted: " ,predicted)

        # print("Predicted Shape: ", predicted.shape)

        print("Score: ", model.score(x_test, y_test))

        return model

    def generate_data_frame_tempeture_corr(self, dataframe):
        """ Recibe un dataframe y retorna un
        archivo con un mapa de temperatura de la correlacion"""
        sns.heatmap(dataframe.corr())
        heatmapIO = io.StringIO()
        plt.savefig(heatmapIO, format='svg')
        plt.close()
        heatmapIO = heatmapIO.getvalue()
        return heatmapIO

    def get(self, request, *args, **kwargs):
        """
            Se recibira por la sesion
            Se recibira fecha
            Lista de materia prima a predecir
        """
        graphics = []  # vector de diccionari con name y fig
        context = super().get_context_data(**kwargs)

        date = datetime.strptime(
            request.session['prediction_date'],
            '%Y-%m-%d'
        )

        raw_materials = json.loads(request.session['prediction_raw_materials'])

        materials_dataframes = self.build_materials_dataframes(raw_materials)
        Xall_df = materials_dataframes[0]
        Xm_df_array = materials_dataframes[1]

        X_dolar = self.build_dolar_dataframes()

        dolar_model = self.train_model(LassoCV(), X_dolar, 'dollar_price')

        print(X_dolar.head())
        graphics.append({
            'name': 'temperatura todos los datos',
            'fig': self.generate_data_frame_tempeture_corr(Xall_df)
        })
        graphics.append({
            'name': 'dolares',
            'fig': self.generate_data_frame_tempeture_corr(X_dolar)
        })

        for key, df in Xm_df_array.items():
            graphics.append(
                {
                    'name': key,
                    'fig': self.generate_data_frame_tempeture_corr(
                        df
                    )
                }
            )

        context['graphics'] = graphics

        context['raw_materials'] = raw_materials

        context['prediction_date'] = date

        return self.render_to_response(context)
