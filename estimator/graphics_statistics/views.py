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

        dolar_prices_cols = [
            {
                'label': 'Fecha',
                'type': 'string'
            },
            {
                'label': 'Precio del dolar en bolívares',
                'type': 'number'
            }
        ]

        dolar_prices_rows = []

        for el in dolar_prices:
            dolar = el.dollar_price
            # if el precio no es en soberano
            if el.date <= self.SOBERANO_DATE:
                dolar = dolar / self.SOBERANO_CHANGE

            dolar_prices_rows.append(
                [
                    el.date.strftime("%m/%d/%Y"),
                    round(dolar, 3)
                ]
            )

        context['dolar_prices_rows'] = dolar_prices_rows
        context['dolar_prices_cols'] = dolar_prices_cols

        return context
