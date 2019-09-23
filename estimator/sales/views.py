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
from django.shortcuts import redirect


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

    def get_context_data(self, **kwargs):
        """Añadiendo variables al contexto """
        context = super().get_context_data(**kwargs)
        context["title"] = "Calendario"
        context["user"] = self.request.user

        context["predictions"] = self.exampleDates()
        context["current_page"] = "calendar_sale"

        return context


class SaleDetailView(DetailView):
    model = Sale
    template_name = "sales/sale_detail.html"

    def get(self, request, *args, **kwargs):
        if self.get_object().company.pk != self.request.user.company.pk:
            return redirect('sales:sales_list')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Contexto de detalle de materia prima"""
        context = super().get_context_data(**kwargs)
        context["current_page"] = "materials"
        return context


class SaleListView(ListView):
    model = Sale
    template_name = "sales/sales_list.html"

    def get_queryset(self):
        new_context = Sale.objects.filter(
            company=self.request.user.company.pk,
        ).order_by('-created')
        return new_context

    def get_context_data(self, **kwargs):
        """Añadiendo variables al contexto """
        context = super().get_context_data(**kwargs)
        context["current_page"] = "calendar_sale"

        return context


class SaleCreateView(CreateView):
    model = Sale
    template_name = "sales/sale_form.html"
    success_url = reverse_lazy("sales:calendar")
    form_class = SaleForm

    def get_form_kwargs(self):
        form_kwargs = super(SaleCreateView, self).get_form_kwargs()

        form_kwargs['user'] = self.request.user

        return form_kwargs

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
        context['unit_system'] = dict(RawMaterial.MEASUREMENT_UNITS)
        context["form_url"] = reverse_lazy('sales:new_material')
        context["current_page"] = "calendar_sale"

        if not self.request.user.is_superuser:
            context["company_user"] = self.request.user.company_user
        context["form_url"] = reverse_lazy('sales:new_sale')
        return context

    def form_invalid(self, form):
        """Si el formulario no es valido retorna el formulario y el contexto"""

        return self.render_to_response(self.get_context_data(
            form=form,
            raw_materials_string=form.data['raw_materials_json']
        ))


class SaleUpdateView(UpdateView):
    model = Sale
    template_name = ".html"


class SaleDeleteView(DeleteView):
    model = Sale
    template_name = ".html"
