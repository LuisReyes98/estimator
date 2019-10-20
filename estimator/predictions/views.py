# from django.shortcuts import render
import copy
import io
import json
from datetime import date, datetime

import category_encoders as ce
import matplotlib
import numpy as np
import pandas as pd
import pytz
import seaborn as sns
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView, TemplateView
from matplotlib import pyplot as plt
from sklearn.linear_model import Lasso, LassoCV
from sklearn.model_selection import cross_val_score, cross_validate

from graphics_statistics.views import \
    generateRawMaterialDolarGraphData as g_graph
from raw_materials.models import RawMaterial
from sales.models import DolarPrice, Sale

from .forms import SelectPredictionForm
from .models import PredictionMaterialRelated, PredictionSale

matplotlib.use('Agg')

"""
20 de agosto de 2018 fue el cambio a bolivar soberano
la moneda se dividio 100.000,00

"""


class PredictionFormView(LoginRequiredMixin, FormView):
    template_name = "predictions/select_prediction.html"
    success_url = reverse_lazy("predictions:result")
    form_class = SelectPredictionForm

    def get_form_kwargs(self):
        form_kwargs = super(PredictionFormView, self).get_form_kwargs()

        form_kwargs['company'] = self.request.user.safe_company
        form_kwargs['request'] = self.request
        return form_kwargs


class PredictionDetailView(LoginRequiredMixin, DetailView):
    model = PredictionSale
    template_name = "predictions/prediction_detail.html"

    def get_context_data(self, **kwargs):
        """Añadiendo variables al contexto """
        context = super().get_context_data(**kwargs)

        graphs = g_graph(
            company=self.request.user.safe_company,
            raw_materials=self.object.raw_materials,
        )

        # context['dolar_graph'] = graphs['dolar_graph']
        context['materials_graph'] = graphs['materials_graph']
        context['graphed_materials'] = graphs['graphed_materials']

        context["current_page"] = "calendar_sale"
        context["report_date"] = datetime.now()

        return context


class PredictionListView(LoginRequiredMixin, ListView):
    model = PredictionSale
    template_name = "predictions/predictions_list.html"
    paginate_by = 30

    def get_queryset(self):
        new_context = PredictionSale.objects.filter(
            company=self.request.user.safe_company
        ).order_by('-created')
        return new_context

    def get_context_data(self, **kwargs):
        """Añadiendo variables al contexto """
        context = super().get_context_data(**kwargs)
        context["current_page"] = "calendar_sale"
        try:
            context["page_counter"] = (int(self.request.GET["page"]) - 1) * self.paginate_by
        except Exception:
            context["page_counter"] = 0

        return context


class PredictionResultView(LoginRequiredMixin, TemplateView):
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
        # print('Train score: ', model.score(xdf, ydf))

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
        # graphics = []  # vector de diccionari con name y fig
        materials_dict = {}
        chart_materials = []
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
            mat = RawMaterial.objects.get(pk=el['pk'])
            chart_materials.append(mat)

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

        for key, df in Xm_df_dict.items():
            """
                Para predecir se requiere el
                - precio del dolar "dollar_price"
                - fecha "date"
            """

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

            # conportamiento porcentual de los valores

            trend_df = df.copy(deep=True)

            res_trend = trend_df.apply(
                lambda x: x.pct_change().mean()
            ).reset_index(name='avg_change').fillna(0)

            # print(res_trend)

            amount_trend = float(
                res_trend.loc[res_trend['index'] == 'amount']['avg_change']
            )
            cost_trend = float(
                res_trend.loc[res_trend['index'] == 'cost_dollar']['avg_change']
            )

            predicted_materials.append({
                'raw_material': materials_dict[key],
                'raw_material_pk': key,
                'cost_dollar': p_dollars,
                'amount': p_amount,
                'amount_trend': amount_trend,
                'cost_trend': cost_trend,
            })




        # predicted_materials
        predicted_materials_array = []
        d_price = round(dolar_prediction[0], 4)

        if self.request.session['prediction_to_save']:
            """Guardando la prediccion"""
            print('Debug saving prediction')
            prediction_sale = PredictionSale(**{
                'prediction_date': prediction_date,
                'company': self.request.user.safe_company,
                'dollar_price': d_price
            })
            prediction_sale.save()
            for pred in predicted_materials:
                c_dollar = round(pred['cost_dollar'][0], 4)
                r_material = RawMaterial.objects.get(pk=pred['raw_material_pk'])

                dict_prediction = {
                        'prediction_date': prediction_date,
                        'amount': int(round(pred['amount'][0])),
                        'cost_dollar': c_dollar,
                        'cost_local': c_dollar * d_price,
                        'dollar_price': d_price,
                        'raw_material': r_material,
                        'prediction_sale': prediction_sale,
                        'amount_trend': pred['amount_trend'],
                        'cost_trend': pred['cost_trend'],
                    }
                pred_material_related = PredictionMaterialRelated(
                    **dict_prediction
                )
                predicted_materials_array.append(dict_prediction)

                pred_material_related.save()
            self.request.session['prediction_to_save'] = False
        else:
            for pred in predicted_materials:
                c_dollar = round(pred['cost_dollar'][0], 4)
                r_material = RawMaterial.objects.get(pk=pred['raw_material_pk'])

                dict_prediction = {
                    'prediction_date': prediction_date,
                    'amount': int(round(pred['amount'][0])),
                    'cost_dollar': c_dollar,
                    'cost_local': c_dollar * d_price,
                    'dollar_price': d_price,
                    'raw_material': r_material,
                    'amount_trend': pred['amount_trend'],
                    'cost_trend': pred['cost_trend'],
                }
                predicted_materials_array.append(dict_prediction)

        graphs = g_graph(
            company=self.request.user.safe_company,
            raw_materials=chart_materials,
        )

        context['materials_graph'] = graphs['materials_graph']

        context['dolar_graph'] = graphs['dolar_graph']

        context['dolar_prediction'] = dolar_prediction

        context['predicted_materials'] = predicted_materials_array

        context['raw_materials'] = raw_materials
        context['materials_dict'] = materials_dict

        context['prediction_date'] = prediction_date

        return self.render_to_response(context)
