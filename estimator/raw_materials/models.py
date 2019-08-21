from django.db import models
from django.utils.translation import ugettext_lazy as translate
# Modelos necesarios para la materia prima


class Provider(models.Model):
    """ Modelo de los proveedores """
    # Campos propios
    # Nombre
    name = models.CharField(
        translate("Name"),
        max_length=50
    )

    # Referencias
    company = models.ForeignKey(
        "users.Company",
        verbose_name=translate("Company"),
        on_delete=models.CASCADE
    )

    raw_materials = models.ManyToManyField(
        "RawMaterial",
        verbose_name=translate("Raw Materials")
    )

    class Meta:
        verbose_name = translate("Provider")
        verbose_name_plural = translate("Providers")

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse("Provider_detail", kwargs={"pk": self.pk})


class RawMaterial(models.Model):
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
        (TON, translate('Ton')),
        (KILOGRAM, translate('Kilograms')),
        (GRAM, translate('grams')),
        (MILLIGRAM, translate('milligrams')),
        (LITER, translate('Liters')),
        (MILLILITER, translate('milliliters')),
        (UNIT, translate('Units')),
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
        translate('name of company'),
        max_length=50,
        blank=False
    )
    # se vence?
    can_expire = models.BooleanField(
        translate('can expire'),
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
        translate('is imported'),
        blank=False,
        default=False,
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    # Campos Referencias
    # Muchos proveedores
    providers = models.ManyToManyField(
        Provider,
        verbose_name=translate("Providers")
    )
    # una compañia
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
