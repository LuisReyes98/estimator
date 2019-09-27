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
    UpdateView,
    FormView)

# from sales.objects import Prediction
from .forms import SaleForm, SaleFileForm
from raw_materials.models import RawMaterial, Provider
from .models import Sale
from django.shortcuts import redirect


class CalendarView(LoginRequiredMixin, TemplateView):
    template_name = "sales/calendar.html"

    # def exampleDates(self):
    #     now = datetime.now()
    #     some_dates = []

    #     for i in range(10):
    #         some_dates.append(
    #             Prediction(
    #                 date=(now - timedelta(days=i)).strftime("%m/%d/%Y"),
    #                 pk=i,
    #             ).__dict__
    #         )

    #     return some_dates

    def get_context_data(self, **kwargs):
        """Añadiendo variables al contexto """
        context = super().get_context_data(**kwargs)
        context["title"] = "Calendario"
        context["user"] = self.request.user

        # context["predictions"] = self.exampleDates()
        context["current_page"] = "calendar_sale"

        return context


class SaleDetailView(DetailView):
    model = Sale
    template_name = "sales/sale_detail.html"

    def get(self, request, *args, **kwargs):
        if self.get_object().company.pk != self.request.user.safe_company.pk:
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
            company=self.request.user.safe_company.pk,
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

    def get_material_providers_json(self, company):
        """Cargando los proveedores de materia prima"""
        result = list(RawMaterial.objects.filter(
                company=self.request.user.safe_company,).values(
                    'measurement_unit',
                    'name',
                    'pk',
                ))
        for counter, value in enumerate(result):
            result[counter]['providers'] = list(Provider.objects.filter(
                rawmaterial=value['pk'],).values(
                    'name',
                    'pk',
                ))
        return json.dumps(list(result), cls=DjangoJSONEncoder)

    def get_context_data(self, **kwargs):
        """User and profile to context"""
        context = super().get_context_data(**kwargs)
        raw_materials = self.get_material_providers_json(self.request.user.safe_company)

        context["raw_materials"] = raw_materials
        context['unit_system'] = dict(RawMaterial.MEASUREMENT_UNITS)
        context["current_page"] = "calendar_sale"

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
    template_name = "sales/sale_form.html"
    success_url = reverse_lazy("sales:calendar")
    form_class = SaleForm

    def form_invalid(self, form):
        """Si el formulario no es valido retorna el formulario y el contexto"""

        return self.render_to_response(self.get_context_data(
            form=form,
            raw_materials_string=form.data['raw_materials_json']
        ))

    def get_form_kwargs(self):
        form_kwargs = super(SaleUpdateView, self).get_form_kwargs()

        form_kwargs['user'] = self.request.user
        form_kwargs['editing'] = True

        return form_kwargs

    def get_material_providers_json(self, company):
        """Cargando los proveedores de materia prima"""
        result = list(RawMaterial.objects.filter(
                company=self.request.user.safe_company,).values(
                    'measurement_unit',
                    'name',
                    'pk',
                ))
        for counter, value in enumerate(result):
            result[counter]['providers'] = list(Provider.objects.filter(
                rawmaterial=value['pk'],).values(
                    'name',
                    'pk',
                ))
        return json.dumps(list(result), cls=DjangoJSONEncoder)

    def build_material(self):
        """ A la hora de editar carga la materia prima en un formato legible por javascript """
        materials_obj = []
        materials_values = []

        for material in self.object.materials_sale_relation:
            materials_values.append(material.raw_material.pk)
            materials_obj.append({
                'pk': material.pk,
                'raw_material_pk': material.raw_material.pk,
                'name': material.raw_material.name,
                'amount': material.amount,
                'measurement_unit': material.raw_material.measurement_unit,
                'bought_in_dollars': material.bought_in_dollars,
                'cost_dollar': material.cost_dollar,
                'cost_local': material.cost_local,
                'provider': material.provider.pk,
                'providers_list': list(Provider.objects.filter(
                    rawmaterial=material.raw_material.pk,).values(
                        'name',
                        'pk',
                )),
            })
        return [
            json.dumps(list(materials_obj), cls=DjangoJSONEncoder),
            json.dumps(list(materials_values), cls=DjangoJSONEncoder),
        ]

    def get_context_data(self, **kwargs):
        """User and profile to context"""
        context = super().get_context_data(**kwargs)

        raw_materials = self.get_material_providers_json(
            self.request.user.safe_company
        )

        # print(self.build_material())
        temp = self.build_material()
        form_materials = temp[0]
        materials_values = temp[1]

        context["raw_materials"] = raw_materials

        context['materials_values'] = materials_values
        context['form_materials'] = form_materials

        context['unit_system'] = dict(RawMaterial.MEASUREMENT_UNITS)
        context["current_page"] = "calendar_sale"
        context["editing"] = True

        context["form_url"] = reverse_lazy(
            'sales:update_sale',
            args=[self.object.pk]
        )
        return context


class SaleDeleteView(DeleteView):
    model = Sale
    template_name = "sales/sale_delete.html"
    success_url = reverse_lazy('sales:sales_list')

    def get(self, request, *args, **kwargs):
        if self.get_object().company.pk != self.request.user.safe_company.pk:
            return redirect('sales:sales_list')
        return super().get(request, *args, **kwargs)


class SaleUploadFileView(FormView):

    template_name = "sales/file_upload.html"
    form_class = SaleFileForm

    success_url = reverse_lazy('sales:calendar')

    def get_form_kwargs(self):
        form_kwargs = super(SaleUploadFileView, self).get_form_kwargs()

        form_kwargs['company'] = self.request.user.safe_company

        return form_kwargs