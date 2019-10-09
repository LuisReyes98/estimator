# from django.shortcuts import render
import io
import json
import copy
from datetime import date, datetime

import category_encoders as ce
import matplotlib
import numpy as np
import pandas as pd
import pytz
import seaborn as sns
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.conf import settings
from matplotlib import pyplot as plt
from sklearn.linear_model import Lasso, LassoCV
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
    tz = pytz.timezone(settings.TIME_ZONE)


    def build_dolar_dataframes(self):
        """ Retorna dataframe de los precios del dolar"""
        dolar_prices = list(
            DolarPrice.objects.filter(
                date__gte=datetime(2018, 8, 19, 0, 0, 0, 0, self.tz)  # fecha despues del cambio de moneda
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
        Xm_df_dict = {}

        for key, value in materials_dict.items():
            df = pd.DataFrame(value)
            df = df.dropna()

            Xm_df_dict[key] = df.drop('raw_material', 1)

        return (Xall_df, Xm_df_dict)

    def train_model(self, model, dataframe, y_column_name):
        # df = dataframe
        ydf = dataframe[y_column_name]
        ydf = ydf.dropna()

        xdf = dataframe.drop(y_column_name, axis=1)
        xdf = xdf.dropna()

        # x_train, x_test, y_train, y_test = train_test_split(xdf, ydf, test_size=0.30)

        # entrenado al modelo

        # model.fit(x_train, y_train)

        # print("Score: ", model.score(x_test, y_test))
        print("X de entrenamiento" ,xdf.head())
        model.fit(xdf, ydf)

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

        prediction_date = datetime.strptime(
            request.session['prediction_date'],
            '%Y-%m-%d'
        )

        prediction_date = prediction_date.replace(tzinfo=self.tz)
        print('prediction_date: ', prediction_date)

        raw_materials = json.loads(request.session['prediction_raw_materials'])
        materials_dict = {}
        for el in raw_materials:
            materials_dict[el['pk']] = el['name']

        materials_dataframes = self.build_materials_dataframes(raw_materials)
        Xall_df = materials_dataframes[0]
        Xm_df_dict = materials_dataframes[1]

        X_dolar = self.build_dolar_dataframes()

        """
        LassoCV(cv=4) 0.81

        para predecir solo necesita la fecha
        """
        dolar_model = self.train_model(
            LassoCV(cv=4),
            X_dolar,
            'dollar_price'
        )
        pred_date = pd.DataFrame([1],[{'date': prediction_date.toordinal()}])
        
        """
            Reshape your data either using array.reshape(-1, 1) if your data has a single feature or array.reshape(1, -1) if it contains a single sample.
        """
        # pred_date = pred_date.reshape(-1, 1)

        print("prediccion dolar: ", dolar_model.predict(
                [{'date': prediction_date.toordinal()}]
            )
        )

        """
        ElasticNet 0.42
        LassoCV(cv=3) 0.48
        """
        # print(Xall_df.head())
        print('all materials cost')

        # modelo de predecir costos usando todas las materias primas
        all_materials_model_cost = self.train_model(
            LassoCV(cv=3),
            Xall_df.drop('amount', axis=1),
            'cost_dollar'
        )

        print('all materials amount')
        # modelos de prediccion de cantidades usando todas las materias primas
        all_materials_model_amount = self.train_model(
            LassoCV(cv=3),
            Xall_df.drop('cost_dollar', axis=1),
            'amount'
        )
        # print(Xall_df.head())

        materials_models_cost_dict = {}
        materials_models_amount_dict = {}

        # graphics.append({
        #     'name': 'temperatura todos los datos',
        #     'fig': self.generate_data_frame_tempeture_corr(Xall_df)
        # })
        # graphics.append({
        #     'name': 'dolares',
        #     'fig': self.generate_data_frame_tempeture_corr(X_dolar)
        # })

        for key, df in Xm_df_dict.items():
            print(materials_dict[key])
            # print(df.head())
            """
            LassoCV(cv=3)
            Lasso() el mas estable de los 3
            ElasticNet()
            """
            """
                Para predecir se requiere el
                - precio del dolar
                - fecha
            """

            # modelo de prediccion de costos de la materia prima seleccionada
            materials_models_cost_dict[key] = self.train_model(
                Lasso(),
                df.drop('amount', axis=1),
                'cost_dollar'
            )
            print(df.drop('amount', axis=1).head)

            # modelo de prediccion de las cantidades seleccionadas
            materials_models_amount_dict[key] = self.train_model(
                Lasso(),
                df.drop('cost_dollar', axis=1),
                'amount'
            )
            print(df.drop('cost_dollar', axis=1).head)

            # print(df.head())

            # graphics.append(
            #     {
            #         'name': materials_dict[key],
            #         'fig': self.generate_data_frame_tempeture_corr(
            #             df
            #         )
            #     }
            # )

        context['graphics'] = graphics

        context['raw_materials'] = raw_materials
        context['materials_dict'] = materials_dict

        context['prediction_date'] = prediction_date

        return self.render_to_response(context)
