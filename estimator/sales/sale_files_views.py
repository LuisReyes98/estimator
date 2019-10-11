import json
import csv
import copy
from datetime import datetime
from django.views.generic import (
    CreateView,
    TemplateView,
)
from .models import Sale, SaleFile, MaterialSaleRelation, DolarPrice
from raw_materials.models import RawMaterial, Provider
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import SaleFileForm
from django.shortcuts import redirect


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
        result = [0, 0, 0, 0]
        try:
            result[0] = datetime.strptime(row[0],'%Y-%m-%d')
        except Exception:
            raise Exception("First column must be a date")

        result[1] = float(row[1])
        result[2] = float(row[2])
        result[3] = float(row[3])

        if result[1] < 0 or result[2] < 0 or result[3] < 0:
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

    def validate_bought(self, bought_in_dollars):
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
        fo = open(file_uploaded.path, 'r')
        reader = csv.reader(fo, 'semi_col')

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

                    sale_data['date'] = first_values[0]
                    sale_data['dollar_price'] = first_values[1]
                    sale_data['total_cost_dollar'] = first_values[2]
                    sale_data['total_cost_local'] = first_values[3]
                    # for i desde la primera coluna numerada
                    for i in range(4, len(row), 6):
                        if row[i] != '':
                            material_data = {}
                            # validacion de la existencia de la materia prima
                            # print(row[i])
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

                    # print(raw_materials_data)
                    # ultimas validaciones
                    if sale_data['total_cost_dollar'] == 0:
                        sale_data['total_cost_dollar'] = total_cost_dollar

                    if sale_data['total_cost_local'] == 0:
                        sale_data['total_cost_local'] = total_cost_local

                    sale_data['dollar_price'] = DolarPrice.objects.create(
                        dollar_price=sale_data['dollar_price'],
                        date=sale_data['date'],
                    )
                    # Guardando la venta
                    sale = Sale.objects.create(**sale_data)

                    for key, value in raw_materials_data.items():
                        value['sale'] = sale
                        material_relation = MaterialSaleRelation.objects.create(**value)

                    counter_success += 1
                except Exception as ex:
                    # se guarda el numero de filas que han fallado y que fila fallo
                    print('Debug: archivo sale_files_views linea 245')
                    print('Debug: error guardando de archivo ', ex)
                    counter_failed += 1
                    failed_rows.append(index + 1)

        fo.close()

        return {
            'counter_success': counter_success,
            'counter_failed': counter_failed,
            'failed_rows': failed_rows,
        }

    def form_valid(self, form):
        self.object = form.save()

        # Guardando la informacion del archivo
        upload_status = self.save_csv_to_sales(self.object.sale_upload, self.request.user)

        # Una vez guardado el archivo a ventas se elimina del servidor
        self.object.sale_upload.delete()

        """ ejemplo del upload_status
            {
                'counter_success': 3,
                'counter_failed': 5,
                'failed_rows': [4, 5, 6, 7, 8]
            }
        """
        params_s = "?counter_success={counter_success}&counter_failed={counter_failed}&failed_rows={failed_rows}".format_map(upload_status)

        return redirect(self.get_success_url() + params_s)


class SaleUploadedFileView(LoginRequiredMixin, TemplateView):
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
