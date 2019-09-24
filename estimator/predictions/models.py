from django.db import models
from estimator.model_mixins import TimeStampFields

from django.utils.translation import ugettext as _
# Create your models here.


class PredictionSale(TimeStampFields):

    prediction_date = models.DateField(
        _("Fecha de Prediccion"),
        auto_now=False,
        auto_now_add=False
    )

    # Referencias
    company = models.ForeignKey(  # Si la registra el superusuario
        'users.Company',
        on_delete=models.SET_NULL,
        parent_link=False,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Prediccion de Venta"
        verbose_name_plural = "Predicciones de Ventas"


class PredicitonMaterialRelated(TimeStampFields):

    prediction_date = models.DateField(
        _("Fecha de Prediccion"),
        auto_now=False,
        auto_now_add=False
    )

    amount = models.PositiveIntegerField(
        _("Cantidad")
    )

    cost_dollar = models.FloatField(
        _("Costo en Dolares"),
    )

    cost_local = models.FloatField(
        _("Costo en la moneda local"),
    )

    # Referencias
    raw_material = models.ForeignKey(
        "raw_materials.RawMaterial",
        verbose_name="Materia prima",
        null=True,
        on_delete=models.SET_NULL,
    )

    prediction_sale = models.ForeignKey(
        PredictionSale,
        verbose_name=_("Prediccion de venta"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Prediccion de Materia Prima"
        verbose_name_plural = "Predicciones de Materias Primas"
