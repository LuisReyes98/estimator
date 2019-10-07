from datetime import datetime

import pytz
from dateutil import tz
from django.db import models
from django.dispatch import receiver
from django.urls import reverse_lazy
from django.utils.translation import ugettext as _

from estimator.model_mixins import TimeStampFields

# Modelos para las ventas


class Sale(TimeStampFields):
    """ Venta de un grupo de productos """
    # campos propios

    total_cost_dollar = models.FloatField(
        "Costo total en dolares",
        blank=True,
    )

    total_cost_local = models.FloatField(
        "Costo total en la moneda local",
        blank=False,
    )

    date = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
    )

    # Referencias
    company = models.ForeignKey(
        'users.Company',
        on_delete=models.SET_NULL,
        parent_link=False,
        blank=True,
        null=True,
    )

    company_user = models.ForeignKey(
        'users.CompanyUser',
        on_delete=models.SET_NULL,
        parent_link=False,
        blank=True,
        null=True,
    )

    raw_materials = models.ManyToManyField(
        "raw_materials.RawMaterial",
        verbose_name="Materias primas",
        through="MaterialSaleRelation",
        through_fields=("sale", "raw_material")
    )

    dollar_price = models.ForeignKey(
        "DolarPrice",
        verbose_name=_("Precio del dolar"),
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"

    @property
    def materials_sale_relation(self):
        """ Obtener el elemento que une a la venta con la materia prima """
        return MaterialSaleRelation.objects.filter(
            sale=self.pk,
        )

    @property
    def date_format(self):
        utc = tz.tzutc()
        local = tz.tzlocal()
        fecha = self.created

        print(fecha)

        local_now = fecha.replace(tzinfo=utc).astimezone(local)

        print(local_now)
        print("--")

        return self.created.replace(tzinfo=utc).astimezone(local)

    def __str__(self):
        return '%s %d' % (self._meta.verbose_name, self.pk)

    def get_absolute_url(self):
        return reverse_lazy("sales:sale", kwargs={"pk": self.pk})


class MaterialSaleRelation(TimeStampFields):
    """ Relacion entre un venta y materia prima para lograr almacenar
    informacion extra """

    # Campos propios
    amount = models.PositiveIntegerField(
        "Cantidad"
    )

    cost_dollar = models.FloatField(
        "Costo en Dolares"
    )

    cost_local = models.FloatField(
        "Costo en la moneda local",
    )

    bought_in_dollars = models.BooleanField(
        _("Comprado en dolares"),
        default=False,
    )

    # Referencias
    raw_material = models.ForeignKey(
        "raw_materials.RawMaterial",
        verbose_name="Materia prima",
        null=True,
        on_delete=models.SET_NULL,
        related_name="sold_ocassions",
        # nombre con el cual se accede a este
        # modelo desde el modelo materia prima (raw material)
    )

    sale = models.ForeignKey(
        "Sale",
        verbose_name="Venta",
        on_delete=models.CASCADE,
        related_name="sold_materials",
    )

    provider = models.ForeignKey(
        "raw_materials.Provider",
        verbose_name=_("Proveedor"),
        on_delete=models.SET_NULL,
        null=True
    )


    class Meta:
        pass


class DolarPrice(TimeStampFields):

    dollar_price = models.FloatField(
        "Precio del dolar",
        blank=False,
        null=False,
    )

    date = models.DateTimeField(
        auto_now=False, 
        auto_now_add=False,
        blank=True,
        null=True,
    )

    def __str__(self):
        return '%.2f' % (self.dollar_price)

    class Meta:
        pass


def get_company_directory_path(instance, filename):
    # el archivo de carga en MEDIA_ROOT/sales/company_<pk>/<filename>

    name = instance.created.strftime('%Y_%m_%d_%H_%M_%S')

    return 'sales/company_{company_pk}/{filename}.csv'.format_map({
        'company_pk': str(instance.company.pk),
        'filename': name
    })


class SaleFile(TimeStampFields):

    FILE_HEADER_FORMAT = (
        'fecha',  # una fecha o 0
        'dolar_precio',  # cualquier flotante
        'total_dolar',  # cualquier flotante
        'total_local',  # cualquier flotante
        'material_~',  # una materia prima de la empresa
        'cantidad_~',  # cualquier entero
        'costo_dolar_~',  # cualquier flotante
        'costo_local_~',  # cualquier flotante
        'comprado_en_dolares_~',  # si,no,No,Si,NO,SI,1,0
        'proveedor_~',  # un proveedor que pertenezca a la materia prima
    )

    sale_upload = models.FileField(
        "Archivo de Registro de Compras",
        upload_to=get_company_directory_path
    )

    # Referencias
    company = models.ForeignKey(  # Si la registra el superusuario
        'users.Company',
        on_delete=models.SET_NULL,
        parent_link=False,
        blank=True,
        null=True,
    )


@receiver(models.signals.post_delete, sender=SaleFile)
def submission_delete(sender, instance, **kwargs):
    instance.sale_upload.delete(False)
