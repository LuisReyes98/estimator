from django.db import models
from django.utils.translation import ugettext_lazy as translate
from estimator.model_mixins import TimeStampFields
from django.urls import reverse_lazy

# Modelos necesarios para la materia prima


class Provider(TimeStampFields):
    """ Modelo de los proveedores """
    # Campos propios
    # Nombre
    name = models.CharField(
        translate("Name"),
        max_length=50,
        blank=False,
    )

    # Referencias
    company = models.ForeignKey(
        "users.Company",
        verbose_name=translate("Company"),
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = translate("Provider")
        verbose_name_plural = translate("Providers")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy("raw_materials:provider", kwargs={"pk": self.pk})


class RawMaterial(TimeStampFields):
    """Modelo de Materia prima"""
    TON = 'T'
    KILOGRAM = 'Kg'
    GRAM = 'g'
    MILLIGRAM = 'mg'
    LITER = 'l'
    MILLILITER = 'ml'
    UNIT = 'u'

    # measurement unit
    MEASUREMENT_UNITS = [
        (TON, 'Toneladas'),
        (KILOGRAM, 'Kilogramos'),
        (GRAM, 'gramos'),
        (MILLIGRAM, 'milligramos'),
        (LITER, 'Litros'),
        (MILLILITER, 'mililitros'),
        (UNIT, 'Unidades'),
    ]

    # Campos propios
    # unidad de medida, en una lista de opciones
    measurement_unit = models.CharField(
        translate("Measurement Unit"),
        max_length=2,
        choices=MEASUREMENT_UNITS,
        default=UNIT,
    )

    # nombre
    name = models.CharField(
        translate('Name'),
        max_length=50,
        blank=False
    )
    # se vence?
    can_expire = models.BooleanField(
        translate('Can expire ?'),
        blank=False,
        default=False,
    )
    # Tiempo en vencerse almacenado como un datetime.timedelta de python
    time_to_expire = models.DurationField(
        translate("Time to expire"),
        blank=True,
    )

    # es importada?
    is_imported = models.BooleanField(
        translate('Is imported ?'),
        blank=False,
        default=False,
    )

    # Campos Referencias
    # Muchos proveedores
    providers = models.ManyToManyField(
        Provider,
        verbose_name=translate("Providers"),
        through="MaterialProvider",
        through_fields=('raw_material', 'provider'),
    )
    # pertenece a una compañia
    company = models.ForeignKey(
        "users.Company",
        verbose_name=translate("Company"),
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = translate("Raw Material")
        verbose_name_plural = translate("Raw Materials")

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse("RawMaterial_detail", kwargs={"pk": self.pk})


class MaterialProvider(models.Model):
    """ Tabla auxiliar de union de mucho a muchos
    de proveedores(provider) con  materia prima(raw material)"""

    provider = models.ForeignKey(
        Provider,
        verbose_name=translate("Provider"),
        on_delete=models.CASCADE,
        related_name="providers"

    )

    raw_material = models.ForeignKey(
        RawMaterial,
        verbose_name=translate("Raw Material"),
        on_delete=models.CASCADE,
        related_name="raw_materials"
    )
