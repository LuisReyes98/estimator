from django.db import models
from django.utils.translation import ugettext_lazy as translate
# Modelos necesarios para la materia prima


class RawMaterial(models.Model):
    """Modelo de Materia prima"""
    KILOGRAM = 'Kg'
    GRAM = 'g'
    MILLIGRAM = 'mg'
    LITER = 'l'
    MILLILITER = 'ml'
    UNIT = 'u'
    # measurement unit
    MEASUREMENT_UNITS = [
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
    # es importada?
    is_imported = models.BooleanField(
        translate('is imported'),
        blank=False,
        default=False,
    )

    class Meta:
        verbose_name = translate("Raw Material")
        verbose_name_plural = translate("Raw Materials")

    # def __str__(self):
    #     return self.name

    # def get_absolute_url(self):
    #     return reverse("RawMaterial_detail", kwargs={"pk": self.pk})
