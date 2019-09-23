from django.db import models
from django.utils.translation import ugettext_lazy as translate
from estimator.model_mixins import TimeStampFields
from django.urls import reverse_lazy
from datetime import timedelta
# Modelos necesarios para la materia prima


class Provider(TimeStampFields):
    """ Modelo de los proveedores """
    # Campos propios
    # Nombre
    name = models.CharField(
        "Nombre",
        max_length=50,
        blank=False,
    )

    # Referencias
    company = models.ForeignKey(
        "users.Company",
        verbose_name="Compañía",
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
    YEAR = timedelta(days=365)
    MONTH = timedelta(days=30)

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
        "Unidad de medida",
        max_length=2,
        choices=MEASUREMENT_UNITS,
        default=UNIT,
    )

    # nombre
    name = models.CharField(
        "Nombre",
        max_length=50,
        blank=False
    )
    # se vence?
    can_expire = models.BooleanField(
        "¿Puede expirar?",
        blank=True,
        default=False,
        # null=True,
    )
    # Tiempo en vencerse almacenado como un datetime.timedelta de python
    time_to_expire = models.DurationField(
        "Tiempo aproximado en expirar",
        blank=True,
        null=True,
    )

    # es importada?
    is_imported = models.BooleanField(
        '¿Es importado?',
        blank=True,
        default=False,
        # null=True,
    )

    # Campos Referencias
    # Muchos proveedores
    providers = models.ManyToManyField(
        Provider,
        verbose_name="Proveedores",
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

    def reduce_days_to_years(self, days):
        return days // 365

    def reduce_days_to_months(self, days):
        while days >= self.YEAR.days:
            days -= 365
        return days // 30

    def extract_year_months_from_days(self, days):
        while days >= self.YEAR.days:
            days -= 365
        while days >= self.MONTH.days:
            days -= 30
        return days

    @property
    def years_to_expire(self):
        if self.time_to_expire is not None:
            days = self.time_to_expire.days
            if days >= self.YEAR.days:
                return self.reduce_days_to_years(days)
        return 0

    @property
    def months_to_expire(self):
        if self.time_to_expire is not None:
            days = self.time_to_expire.days
            if days > 30:
                return self.reduce_days_to_months(days)
            else:
                return 0
        return 0

    @property
    def days_to_expire(self):
        if self.time_to_expire is not None:
            days = self.time_to_expire.days
            return self.extract_year_months_from_days(days)
        return 0

    @property
    def unit_name(self):
        units = dict(self.MEASUREMENT_UNITS)
        return units[self.measurement_unit]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy("raw_materials:material", kwargs={"pk": self.pk})


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
