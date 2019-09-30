import json
import csv
import copy
from datetime import datetime, timedelta

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
)
from django.http import HttpResponseRedirect
from .forms import SaleForm, SaleFileForm, DolarPrice
from raw_materials.models import RawMaterial, Provider
from .models import Sale, SaleFile, MaterialSaleRelation
from django.shortcuts import redirect, render


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


class SaleDetailView(LoginRequiredMixin, DetailView):
    model = Sale
    template_name = "sales/sale_detail.html"

    def get(self, request, *args, **kwargs):
        if self.get_object().company.pk != self.request.user.safe_company.pk:
            return redirect('sales:sales_list')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Contexto de detalle de materia prima"""
        context = super().get_context_data(**kwargs)
        context["current_page"] = "calendar_sale"
        return context


class SaleListView(LoginRequiredMixin, ListView):
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


class SaleCreateView(LoginRequiredMixin, CreateView):
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


class SaleUpdateView(LoginRequiredMixin, UpdateView):
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


class SaleDeleteView(LoginRequiredMixin, DeleteView):
    model = Sale
    template_name = "sales/sale_delete.html"
    success_url = reverse_lazy('sales:sales_list')

    def get(self, request, *args, **kwargs):
        if self.get_object().company.pk != self.request.user.safe_company.pk:
            return redirect('sales:sales_list')
        return super().get(request, *args, **kwargs)


class SaleUploadFileView(LoginRequiredMixin, CreateView):
    model = SaleFile
    template_name = "sales/file_upload.html"
    form_class = SaleFileForm

    success_url = reverse_lazy('sales:uploaded_file')

    def get_context_data(self, **kwargs):
        """User and profile to context"""
        context = super().get_context_data(**kwargs)
        context["current_page"] = "calendar_sale"
        context["materials_ex"] = RawMaterial.objects.filter(
            company=self.request.user.safe_company.pk,
        )
        context["providers_ex"] = Provider.objects.filter(
            company=self.request.user.safe_company.pk,
        )

        context["download_url"] = '/static/files/sales/upload_format.csv'

        return context

    def get_form_kwargs(self):
        form_kwargs = super(SaleUploadFileView, self).get_form_kwargs()

        form_kwargs['company'] = self.request.user.safe_company

        return form_kwargs

    def parse_row_to_materials_sale(self, row, company):
        pass

    def validate_first_cols(self, row):
        result = [0, 0, 0]
        result[0] = float(row[0])
        result[1] = float(row[1])
        result[2] = float(row[2])

        if result[0] < 0 or result[1] < 0 or result[2] < 0:
            raise Exception("No se permiten valores negativos")

        return result

    def validate_provider(self, value, raw_material):
        # print(value)
        try:
            # primero busca por nombre
            temp_provider = Provider.objects.get(
                name=value,
                rawmaterial=raw_material
            )
        except Exception:
            # luego busca por id
            temp_provider = Provider.objects.get(
                pk=int(value),
                rawmaterial=raw_material
            )

        return temp_provider

    def validate_material(self, value, company):
        try:
            # primero busca por nombre
            temp_material = RawMaterial.objects.get(
                name=value,
                company=company
            )
        except Exception:
            # luego busca por id
            temp_material = RawMaterial.objects.get(
                pk=int(value),
                company=company
            )

        return temp_material

    def validate_bought(self,bought_in_dollars):
        result = False
        int_value = False

        try:
            result = int(bought_in_dollars)
            int_value = True

        except Exception:
            result = bought_in_dollars.upper()

        if int_value:
            if result == 1:
                result = True
            elif result == 0:
                result = False
            else:
                raise Exception('Valor no valido')
        else:
            if result == 'SI':
                result = True
            elif result == 'NO':
                result = False
            else:
                raise Exception('Valor no valido')

        return result

    def validate_amount_costs(self, amount, cost_dollar, cost_local, bought_in_dollars, dollar_price):

        result = {}
        result['amount'] = int(amount)
        result['cost_dollar'] = float(cost_dollar)
        result['cost_local'] = float(cost_local)

        if result['amount'] < 1 or result['cost_dollar'] < 0 or result['cost_local'] < 0:
            raise Exception("No se aceptan numeros negativos")

        result['bought_in_dollars'] = self.validate_bought(bought_in_dollars)

        if result['bought_in_dollars']:
            result['cost_local'] = result['cost_dollar'] * result['amount'] * dollar_price
        else:
            result['cost_dollar'] = result['cost_local'] * result['amount'] / dollar_price

        return result

    def save_csv_to_sales(self, file_uploaded, user):
        """
            Razones para no guardar una venta
            faltan valores
            una materia prima se repite
            el proveedor no pertenece a la materia prima
            el valor de la columna no es valido
        """
        csv.register_dialect('semi_col', delimiter=';', quoting=csv.QUOTE_NONE)
        reader = csv.reader(open(file_uploaded.path, 'r'), 'semi_col')

        counter_success = 0
        counter_failed = 0
        failed_rows = []
        company = user.safe_company
        if not user.is_superuser:
            company_user = user.companyuser
        else:
            company_user = None

        for index, row in enumerate(reader):
            sale_data = {}
            materials_count = 0
            if index > 0:
                try:
                    total_cost_dollar = 0
                    total_cost_local = 0
                    raw_materials_data = {}

                    sale_data['company'] = company
                    if company_user:
                        sale_data['company_user'] = company_user

                    first_values = self.validate_first_cols(row)

                    sale_data['dollar_price'] = first_values[0]
                    sale_data['total_cost_dollar'] = first_values[1]
                    sale_data['total_cost_local'] = first_values[2]

                    for i in range(3, len(row), 6):
                        if row[i] != '':
                            material_data = {}
                            # validacion de la existencia de la materia prima
                            temp_material = self.validate_material(
                                row[i], company
                            )
                            material_data['raw_material'] = temp_material

                            amount_costs = self.validate_amount_costs(
                                row[i + 1],
                                row[i + 2],
                                row[i + 3],
                                row[i + 4],
                                sale_data['dollar_price'],
                            )
                            material_data['amount'] = amount_costs['amount']

                            material_data['cost_dollar'] = amount_costs['cost_dollar']

                            material_data['cost_local'] = amount_costs['cost_local']

                            material_data['bought_in_dollars'] = amount_costs['bought_in_dollars']

                            # valor calculado de la compra
                            total_cost_dollar += material_data['amount'] * material_data['cost_dollar']

                            total_cost_local += material_data['amount'] * material_data['cost_local']

                            material_data['provider'] = self.validate_provider(
                                row[i + 5],
                                temp_material
                            )
                            # que no existan materia prima repetida
                            if raw_materials_data.get(temp_material.pk):
                                raise Exception("Materia prima repetida")
                            else:
                                raw_materials_data[temp_material.pk] = copy.copy(material_data)
                            materials_count += 1

                    if materials_count < 1:
                        raise Exception("No hay materia prima suficiente")

                    print(raw_materials_data)
                    # ultimas validaciones
                    if sale_data['total_cost_dollar'] == 0:
                        sale_data['total_cost_dollar'] = total_cost_dollar

                    if sale_data['total_cost_local'] == 0:
                        sale_data['total_cost_local'] = total_cost_local

                    sale_data['dollar_price'] = DolarPrice.objects.create(dollar_price=sale_data['dollar_price'])
                    # Guardando la venta
                    sale = Sale.objects.create(**sale_data)

                    for key, value in raw_materials_data.items():
                        value['sale'] = sale
                        material_relation = MaterialSaleRelation.objects.create(**value)

                    counter_success += 1
                except Exception as ex:
                    # print("no se proceso ")
                    # print(ex)
                    # print(row)
                    counter_failed += 1
                    failed_rows.append(index + 1)

        return {
            'counter_success': counter_success,
            'counter_failed': counter_failed,
            'failed_rows': failed_rows,
        }

    def form_valid(self, form):
        self.object = form.save()

        # uploaded file
        #self.object.sale_upload

        #read the file
        # self.object.sale_upload.read()
        upload_status = self.save_csv_to_sales(self.object.sale_upload, self.request.user)

        # print('Result:', upload_status)
        # Una vez tranformado el archivo a ventas se elimina del servidor
        self.object.sale_upload.delete()

        """'counter_success': 3, 'counter_failed': 5, 'failed_rows': [4, 5, 6, 7, 8]"""
        params_s = "?counter_success={counter_success}&counter_failed={counter_failed}&failed_rows={failed_rows}".format_map(upload_status)

        return redirect(self.get_success_url() + params_s)


class SaleUploadedFileView(TemplateView):
    template_name = "sales/file_uploaded.html"

    def get_context_data(self, **kwargs):
        """User and profile to context"""
        print(kwargs)
        context = super().get_context_data(**kwargs)
        context["current_page"] = "calendar_sale"

        return context

    def get(self, request, *args, **kwargs):
        """añadiendo variables al contexto en get"""
        context = self.get_context_data(**kwargs)
        context["counter_success"] = request.GET.get("counter_success")
        context["counter_failed"] = request.GET.get("counter_failed")
        context["failed_rows"] = json.loads(request.GET.get("failed_rows"))

        return self.render_to_response(context)
