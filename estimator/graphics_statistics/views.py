import pytz
from datetime import datetime
from django.conf import settings

from django.shortcuts import render
from django.views.generic import TemplateView
from sales.models import DolarPrice, Sale
from raw_materials.models import RawMaterial
from predictions.models import PredictionSale


class GraphicsView(TemplateView):
    template_name = "graphics/graphics.html"
    tz = pytz.timezone(settings.TIME_ZONE)
    SOBERANO_CHANGE = 100000.00
    # fechas menores o igual a esta ocurrieron antes del cambio de moneda
    SOBERANO_DATE = datetime(2018, 8, 18, 0, 0, 0, 0, tz)

    def get_context_data(self, **kwargs):
        """Añadiendo variables al contexto """
        dolar_prices_series = {}

        dolar_prices_series['series'] = []
        context = super().get_context_data(**kwargs)

        dolar_prices = list(
            DolarPrice.objects.exclude(
                date__isnull=True
            ).order_by('date')
        )

        predicted_sales = PredictionSale.objects.filter(
            company=self.request.user.safe_company
        )
        sales = Sale.objects.filter(
            company=self.request.user.safe_company.pk,
        ).exclude(
            date__isnull=True,
            raw_materials__isnull=True,
            dollar_price__isnull=True,
        ).order_by('date')

        raw_materials = RawMaterial.objects.filter(
            company=self.request.user.safe_company.pk,
        )
        materials_graph = {}
        materials_options = []

        raw_materials_dict = {}
        # rellenar diccionario por cada materia prima de la empresa
        for mat in raw_materials:
            raw_materials_dict[mat.pk] = {
                'name': mat.name,
                'pk': mat.pk,
                'unit': mat.unit_name,
                'dolar_cost': [],
                'local_cost': [],
                'amount': [],
                'pred_dolar_cost': [],
                'pred_local_cost': [],
                'pred_amount': [],
            }

        # cargando los datos de los precios del dolar registrados
        dollar_data = []
        for el in dolar_prices:
            dolar = el.dollar_price
            # if el precio no es en soberano
            if el.date <= self.SOBERANO_DATE:
                dolar = dolar / self.SOBERANO_CHANGE

            dollar_data.append(
                [
                    el.date.strftime("%m/%d/%Y"),
                    round(dolar, 3)
                ]
            )
        # agregando la serie al arreglo
        dolar_prices_series['series'].append(
            {
                'name': 'Precio registrado del Dolar',
                'data': dollar_data,
            }
        )

        predicted_dollar_data = []
        # cargando los datos de los precios del dolar predicho
        for el in predicted_sales:
            # por cada  grupo de compras predicho
            predicted_dollar_data.append(
                [
                    el.prediction_date.strftime("%m/%d/%Y"),
                    round(el.dollar_price, 3)
                ]
            )

            for predic in el.predictions:
                # por cada materia prima predicha
                raw_materials_dict[predic.raw_material.pk]['pred_dolar_cost'].append(
                    [
                        predic.prediction_date.strftime("%m/%d/%Y"),
                        round(predic.cost_dollar, 3)
                    ]
                )
                raw_materials_dict[predic.raw_material.pk]['pred_local_cost'].append(
                    [
                        predic.prediction_date.strftime("%m/%d/%Y"),
                        round(predic.cost_local, 3)
                    ]
                )
                raw_materials_dict[predic.raw_material.pk]['pred_amount'].append(
                    [
                        predic.prediction_date.strftime("%m/%d/%Y"),
                        predic.amount
                    ]
                )

        # agregando la serie al arreglo
        dolar_prices_series['series'].append(
            {
                'name': 'Precio estimado del Dolar',
                'data': predicted_dollar_data,
            }
        )
        # datos de configuracion
        dolar_prices_series['yaxis_title'] = 'Precio del dolar'
        dolar_prices_series['title'] = 'Precio del dolar a lo largo del tiempo'

        # por cada venta realiza cargar los datos
        for sale in sales:
            for material_relation in sale.materials_sale_relation:
                raw_materials_dict[material_relation.raw_material.pk]['dolar_cost'].append(
                    [
                        sale.date.strftime("%m/%d/%Y"),
                        round(material_relation.cost_dollar, 3)
                    ]
                )
                raw_materials_dict[material_relation.raw_material.pk]['local_cost'].append(
                    [
                        sale.date.strftime("%m/%d/%Y"),
                        round(material_relation.cost_local, 3)
                    ]
                )
                raw_materials_dict[material_relation.raw_material.pk]['amount'].append(
                    [
                        sale.date.strftime("%m/%d/%Y"),
                        material_relation.amount
                    ]
                )

        for key, value in raw_materials_dict.items():
            if (len(value['dolar_cost']) > 0):
                
                dolar_data = []
                dolar_data.append(
                    {
                        'name': 'Costo en compra en dolares',
                        'data': value['dolar_cost']
                    }
                )
                dolar_data.append(
                    {
                        'name': 'Costo predicho en dolares',
                        'data': value['pred_dolar_cost']
                    }
                )
                local_data = []
                local_data.append(
                    {
                        'name': 'Costo en compra en bolívares',
                        'data': value['local_cost']
                    }
                )
                local_data.append(
                    {
                        'name': 'Costo predicho en bolívares',
                        'data': value['pred_local_cost']
                    }
                )

                amount_data = []
                amount_data.append(
                    {
                        'name': 'Cantidad en compra',
                        'data': value['amount']
                    }
                )
                amount_data.append(
                    {
                        'name': 'Cantidad predicha',
                        'data': value['pred_amount']
                    }
                )
                materials_options.append(
                    {
                        'name': value['name'],
                        'key': value['pk'],
                    }
                )

                materials_graph[key] = {
                    'name': value['name'],
                    'key': value['pk'],
                    'graphs': [
                        {
                            'series': dolar_data,
                            'yaxis_title': 'Costos en dolares',
                            'title': 'Costos en dolares por %s de %s' % (
                                value['unit'],
                                value['name'],
                            ),
                        },
                        {
                            'series': local_data,
                            'yaxis_title': 'Costos en bolívares',
                            'title': 'Costos en bolívares por %s de %s' % (
                                value['unit'],
                                value['name'],
                            ),
                        },
                        {
                            'series': amount_data,
                            'yaxis_title': 'Cantidad de %s' % (value['unit']),
                            'title': 'Cantidad de %s por compra de %s' % (
                                value['unit'],
                                value['name'],
                            ),
                        }
                    ]
                }

        context['materials_graph'] = materials_graph
        context['materials_options'] = materials_options

        context['dolar_prices_series'] = dolar_prices_series

        return context
