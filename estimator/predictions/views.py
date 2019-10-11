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
        materials_dict = {}
        # materials_values = []
        # all_materials_array = []
        # contruyendo grupos de datos

        sales = list(Sale.objects.filter(
            company=self.request.user.safe_company.pk,
        ).exclude(
                date__isnull=True,
                raw_materials__isnull=True,
                dollar_price__isnull=True,
            ).order_by('date')
        )

        # raw_materials_query = RawMaterial.objects.filter(
        #     company=self.request.user.safe_company.pk
        # )
        # # dataframe de todas las materias primas
        # for mat in raw_materials_query:
        #     materials_values.append(mat.pk)

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
                # all_materials_array.append(value)
                if material.raw_material.pk in materials_dict:
                    materials_dict[material.raw_material.pk].append(
                        value
                    )

        # Xall_df = pd.DataFrame(all_materials_array)

        # Xall_df = Xall_df.dropna()

        # codificador de categorias (nombre de materia prima)
        # Xall_df = self.encoding_raw_material(
        #     'raw_material',
        #     Xall_df,
        #     materials_values
        # )

        # diccionario de dataframes de las materias primas seleccionadas
        Xm_df_dict = {}

        for key, value in materials_dict.items():
            df = pd.DataFrame(value)
            df = df.dropna()

            Xm_df_dict[key] = df.drop('raw_material', 1)

        return Xm_df_dict

    def train_model(self, model, dataframe, y_column_name):
        ydf = dataframe[y_column_name]
        ydf = ydf.dropna()

        xdf = dataframe.drop(y_column_name, axis=1)
        xdf = xdf.dropna()

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

    # def predict_dolar(self, date)
    def encoding_raw_material(self, column_name, dataframe, columns_values):
        df = copy.copy(dataframe)

        for val in columns_values:
            new_col_name = column_name + '_' + str(val)
            df[new_col_name] = (df[column_name] == val).astype(int)

        return df.drop(column_name, 1)

    def get(self, request, *args, **kwargs):
        """
            Se recibira por la sesion
            Se recibira fecha
            Lista de materia prima a predecir
        """
        graphics = []  # vector de diccionari con name y fig
        context = super().get_context_data(**kwargs)
        materials_dict = {}
        predicted_materials = []
        predicted_materials_by_all = []
        materials_models_cost_dict = {}
        materials_models_amount_dict = {}

        prediction_date = datetime.strptime(
            request.session['prediction_date'],
            '%Y-%m-%d'
        )

        prediction_date = prediction_date.replace(tzinfo=self.tz)
        # print('prediction_date: ', prediction_date)

        raw_materials = json.loads(request.session['prediction_raw_materials'])

        for el in raw_materials:
            materials_dict[el['pk']] = el['name']

        # materials_dataframes = self.build_materials_dataframes(raw_materials)

        # Xall_df = materials_dataframes[0]
        Xm_df_dict = self.build_materials_dataframes(raw_materials)
        # materials_values = materials_dataframes[2]

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

        pred_df_date = prediction_date.toordinal()
        prediction_df = pd.DataFrame(
            [{'date': pred_df_date} for i in range(4)]
        )

        dolar_prediction = dolar_model.predict(
            prediction_df
        )
        prediction_df['dollar_price'] = dolar_prediction

        """
            Para predecir necesitan
            fecha
            precio del dolar
            materia prima encodeada a binario

            LassoCV(cv=3) 0.48
        """
        # modelo de predecir costos usando todas las materias primas
        # all_materials_model_cost = self.train_model(
        #     LassoCV(cv=3),
        #     Xall_df.drop('amount', axis=1),
        #     'cost_dollar'
        # )

        # modelos de prediccion de cantidades usando todas las materias primas
        """
            para predecir
            Lasso Cross Validation
        """
        # all_materials_model_amount = self.train_model(
        #     LassoCV(cv=3),
        #     Xall_df.drop('cost_dollar', axis=1),
        #     'amount'
        # )

        # for el in raw_materials:
        #     # for each material create a df to predict its value
        #     temp_df = copy.copy(prediction_df)  # clona el valor del df
        #     # genera un arreglo para la materia priam
        #     temp_df['raw_material'] = el['pk']  # agrega el arreglo al df
        #     temp_df = self.encoding_raw_material(
        #         'raw_material',
        #         temp_df,
        #         materials_values
        #     )
        #     p_dollars_all = all_materials_model_cost.predict(temp_df)
        #     p_amount_all = all_materials_model_amount.predict(temp_df)
        #     predicted_materials_by_all.append({
        #         'raw_material': el['pk'],
        #         'cost_collar': p_dollars_all,
        #         'amount': p_amount_all,
        #     })

        print(prediction_df)
        # print(predicted_materials_by_all)
        # graphics.append({
        #     'name': 'temperatura todos los datos',
        #     'fig': self.generate_data_frame_tempeture_corr(Xall_df)
        # })

        # graphics.append({
        #     'name': 'dolares',
        #     'fig': self.generate_data_frame_tempeture_corr(X_dolar)
        # })

        for key, df in Xm_df_dict.items():
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

            # modelo de prediccion de las cantidades seleccionadas
            materials_models_amount_dict[key] = self.train_model(
                Lasso(),
                df.drop('cost_dollar', axis=1),
                'amount'
            )
            p_dollars = materials_models_cost_dict[key].predict(prediction_df)
            p_amount = materials_models_amount_dict[key].predict(prediction_df)
            predicted_materials.append({
                'raw_material': key,
                'cost_collar': p_dollars,
                'amount': p_amount,
            })

            # predicted_materials

        context['graphics'] = graphics

        context['dolar_prediction'] = dolar_prediction

        # context['predicted_materials_by_all'] = predicted_materials_by_all
        
        context['predicted_materials'] = predicted_materials

        context['raw_materials'] = raw_materials
        context['materials_dict'] = materials_dict

        context['prediction_date'] = prediction_date

        return self.render_to_response(context)
