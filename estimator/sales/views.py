from datetime import datetime, timedelta
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView)

from sales.objects import Prediction
from .forms import SaleForm
from raw_materials.models import RawMaterial
from .models import Sale

# Create your views here.


class CalendarView(LoginRequiredMixin, TemplateView):
    template_name = "sales/calendar.html"

    def exampleDates(self):
        now = datetime.now()
        some_dates = []

        for i in range(10):
            some_dates.append(
                Prediction(
                    date=(now - timedelta(days=i)).strftime("%m/%d/%Y"),
                    pk=i,
                ).__dict__
            )

        return some_dates

    def get(self, request, *args, **kwargs):

        """añadiendo variables al contexto en get"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Calendario"
        context["user"] = self.request.user

        context["predictions"] = self.exampleDates()

        return self.render_to_response(context)


class SaleDetailView(DetailView):
    model = Sale
    template_name = ".html"


class SaleListView(ListView):
    model = Sale
    template_name = ".html"


class SaleCreateView(CreateView):
    model = Sale
    template_name = "sales/sale_form.html"
    success_url = reverse_lazy("sales:calendar")
    form_class = SaleForm

    def get_context_data(self, **kwargs):
        """User and profile to context"""
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["company"] = self.request.user.company

        context["raw_materials"] = json.dumps(
            list(RawMaterial.objects.filter(
                company=self.request.user.company,).values(
                    'measurement_unit',
                    'name',
                    'pk',
                )
            ), cls=DjangoJSONEncoder
        )
        context["unit_system"] = dict(RawMaterial.MEASUREMENT_UNITS)
        if not self.request.user.is_superuser:
            context["company_user"] = self.request.user.company_user
        context["form_url"] = reverse_lazy('sales:new_sale')
        return context


class SaleUpdateView(UpdateView):
    model = Sale
    template_name = ".html"


class SaleDeleteView(DeleteView):
    model = Sale
    template_name = ".html"
