import pytz
from datetime import datetime
from django.conf import settings

from django.shortcuts import render
from django.views.generic import TemplateView
from sales.models import DolarPrice


class GraphicsView(TemplateView):
    template_name = "graphics/graphics.html"
    tz = pytz.timezone(settings.TIME_ZONE)
    SOBERANO_CHANGE = 100000.00
    # fechas menores o igual a esta ocurrieron antes del cambio de moneda
    SOBERANO_DATE = datetime(2018, 8, 18, 0, 0, 0, 0, tz)

    def get_context_data(self, **kwargs):
        """Añadiendo variables al contexto """
        context = super().get_context_data(**kwargs)

        dolar_prices = list(
            DolarPrice.objects.exclude(
                date__isnull=True
            ).order_by('date')
        )

        dolar_prices_series = {}

        dolar_prices_series['series'] = []

        dollar_data = []
        for index, el in enumerate(dolar_prices):
            if index == 0:
                dolar_prices_series['first_date'] = el.date.strftime("%m/%d/%Y")
            dolar = el.dollar_price
            # if el precio no es en soberano
            if el.date <= self.SOBERANO_DATE:
                dolar = dolar / self.SOBERANO_CHANGE

            dollar_data.append([el.date.strftime("%m/%d/%Y"),round(dolar, 3)])

        dolar_prices_series['series'].append(
            {
                'name': 'Precio del Dolar',
                'data': dollar_data,
            }
        )
        dolar_prices_series['yaxis_title'] = 'Precio del dolar'
            
        dolar_prices_series['title'] = 'Precio del dolar a lo largo del tiempo'

        context['dolar_prices_series'] = dolar_prices_series

        return context
