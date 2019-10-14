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
from sklearn.model_selection import (cross_val_score, cross_validate)

from raw_materials.models import RawMaterial
from sales.models import DolarPrice, Sale

from .models import PredictionSale, PredicitonMaterialRelated
from .forms import SelectPredictionForm

matplotlib.use('Agg')

"""
20 de agosto de 2018 fue el cambio a bolivar soberano
la moneda se dividio 100.000,00

"""


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
    SOBERANO_CHANGE = 100000.00
    # fechas menores o igual a esta ocurrieron antes del cambio de moneda
    SOBERANO_DATE = datetime(2018, 8, 18, 0, 0, 0, 0, tz)

    def build_dolar_dataframes(self):
        """ Retorna dataframe de los precios del dolar"""
        dolar_prices = list(
            DolarPrice.objects.exclude(
                date__isnull=True
            ).order_by('date')
        )

        dolar_prices_array = []

        for el in dolar_prices:
            dolar = el.dollar_price
            # if el precio no es en soberano
            if el.date <= self.SOBERANO_DATE:
                dolar = dolar / self.SOBERANO_CHANGE

            dolar_prices_array.append({
                'date': el.date.toordinal(),
                'dollar_price': dolar
            })
        # print(dolar_prices_array)

        xdf = pd.DataFrame(dolar_prices_array)
        xdf.dropna()

        return xdf

    def build_materials_dataframes(self, raw_materials):
        materials_dict = {}
        # contruyendo grupos de datos

        sales = list(Sale.objects.filter(
            company=self.request.user.safe_company.pk,
        ).exclude(
                date__isnull=True,
                raw_materials__isnull=True,
                dollar_price__isnull=True,
            ).order_by('date')
        )

        for material in raw_materials:
            materials_dict[material['pk']] = []
        # construyendo diccionario de datos a utilizar

        for sale in sales:
            for material in sale.materials_sale_relation:
                dolar = sale.dollar_price.dollar_price
                if sale.date <= self.SOBERANO_DATE:
                    dolar = dolar / self.SOBERANO_CHANGE

                value = {
                            'cost_dollar': material.cost_dollar,
                            'amount': material.amount,
                            'raw_material': material.raw_material.pk,
                            'dollar_price': dolar,
                            'date': sale.date.toordinal(),
                        }
                # all_materials_array.append(value)
                if material.raw_material.pk in materials_dict:
                    materials_dict[material.raw_material.pk].append(
                        value
                    )

        # diccionario de dataframes de las materias primas seleccionadas
        Xm_df_dict = {}

        for key, value in materials_dict.items():
            df = pd.DataFrame(value)
            df = df.dropna()

            Xm_df_dict[key] = df.drop('raw_material', 1)

        return Xm_df_dict

    def train_model(self, model, dataframe, y_column_name, x_column_name='x',two_value_prediction=False):
        if two_value_prediction:
            ydf = dataframe[y_column_name].values.reshape(-1, 1)
            xdf = dataframe[x_column_name].values.reshape(-1, 1)

        else:
            ydf = dataframe[y_column_name]
            xdf = dataframe.drop(y_column_name, axis=1)

            ydf = ydf.dropna()
            xdf = xdf.dropna()

        model.fit(xdf, ydf)
        print('Train score: ', model.score(xdf, ydf))

        return model

    def generate_linear_plot(self, x_col_name, y_col_name, dataframe):
        pass
        sns.lmplot(x=x_col_name, y=y_col_name, data=dataframe)
        fileIO = io.StringIO()
        plt.savefig(fileIO, format='svg')
        plt.close()
        fileIO = fileIO.getvalue()

        return fileIO

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
        context = super().get_context_data(**kwargs)
        graphics = []  # vector de diccionari con name y fig
        materials_dict = {}
        predicted_materials = []
        materials_models_cost_dict = {}
        materials_models_amount_dict = {}
        raw_materials = json.loads(request.session['prediction_raw_materials'])

        prediction_date = datetime.strptime(
            request.session['prediction_date'],
            '%Y-%m-%d'
        )

        prediction_date = prediction_date.replace(tzinfo=self.tz)

        for el in raw_materials:
            materials_dict[el['pk']] = el['name']

        Xm_df_dict = self.build_materials_dataframes(raw_materials)

        X_dolar = self.build_dolar_dataframes()

        """
        LassoCV(cv=4) 0.81
        LinearRegression
        para predecir solo  necesita la fecha
        """
        # LassoCV(cv=4),
        dolar_model = self.train_model(
            LassoCV(cv=4, positive=True),
            X_dolar,
            'dollar_price',
            # x_column_name='date',
            # two_value_prediction=True,
        )

        pred_df_date = prediction_date.toordinal()
        prediction_df = pd.DataFrame(
            [{'date': pred_df_date} for i in range(2)]
        )

        dolar_prediction = dolar_model.predict(
            prediction_df
        )

        # prediction_df['dollar_price'] = dolar_prediction

        # print(prediction_df)
        graphics.append({
            'name': "Precio del dolar",
            'fig': self.generate_linear_plot('date', 'dollar_price', X_dolar)
        })

        for key, df in Xm_df_dict.items():
            """
                Para predecir se requiere el
                - precio del dolar "dollar_price"
                - fecha "date"
            """

            graphics.append({
                'name': materials_dict[key] + " costo",
                'fig': self.generate_linear_plot('date', 'cost_dollar', df)
            })
            graphics.append({
                'name': materials_dict[key] + " cantidad",
                'fig': self.generate_linear_plot('date', 'amount', df)
            })

            # print(df.shape)
            # modelo de prediccion de costos de la materia prima seleccionada
            # LinearRegression(),
            materials_models_cost_dict[key] = self.train_model(
                Lasso(positive=True),
                df.drop(['amount','dollar_price'], axis=1),
                'cost_dollar'
            )

            # modelo de prediccion de las cantidades seleccionadas
            # LinearRegression(),
            materials_models_amount_dict[key] = self.train_model(
                Lasso(positive=True),
                df.drop(['cost_dollar','dollar_price'], axis=1),
                'amount'
            )
            p_dollars = materials_models_cost_dict[key].predict(prediction_df)
            p_amount = materials_models_amount_dict[key].predict(prediction_df)

            if p_amount[0] < 1:
                p_amount[0] = 1

            predicted_materials.append({
                'raw_material': materials_dict[key],
                'raw_material_pk': key,
                'cost_dollar': p_dollars,
                'amount': p_amount,
            })

            # predicted_materials
        if self.request.session['prediction_to_save']:
            print('Debug saving prediction')
            prediction_sale = PredictionSale(**{
                'prediction_date': prediction_date,
                'company': self.request.user.safe_company
            })
            prediction_sale.save()

            for pred in predicted_materials:
                d_price = round(dolar_prediction[0], 4)
                c_dollar = round(pred['cost_dollar'][0], 4)
                r_material = RawMaterial.objects.get(pk=pred['raw_material_pk'])

                pred_material_related = PredicitonMaterialRelated(
                    **{
                        'prediction_date': prediction_date,
                        'amount': round(pred['amount'][0]),
                        'cost_dollar': c_dollar,
                        'cost_local': c_dollar * d_price,
                        'dollar_price': d_price,
                        'raw_material': r_material,
                        'prediction_sale': prediction_sale,
                    }
                )
                pred_material_related.save()
            self.request.session['prediction_to_save'] = False

        context['graphics'] = graphics

        context['dolar_prediction'] = dolar_prediction

        context['predicted_materials'] = predicted_materials

        context['raw_materials'] = raw_materials
        context['materials_dict'] = materials_dict

        context['prediction_date'] = prediction_date

        return self.render_to_response(context)
