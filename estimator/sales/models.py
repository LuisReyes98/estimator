from django.db import models
from django.utils.translation import ugettext_lazy as translate
from estimator.model_mixins import TimeStampFields
# Modelos para las ventas


class Sale(TimeStampFields):
    """ Venta de un grupo de productos """
    # campos propios

    total_cost_dollar = models.FloatField(
        "Costo total en dolares"
    )

    total_cost_local = models.FloatField(
        "Costo total en la moneda local",
    )

    # Referencias
    company = models.ForeignKey(  # Si la registra el superusuario
        'users.Company',
        on_delete=models.SET_NULL,
        parent_link=True,
        blank=True,
        null=True,
    )

    company_user = models.ForeignKey(  # Si la registra un admin
        'users.CompanyUser',
        on_delete=models.SET_NULL,
        parent_link=True,
        blank=True,
        null=True,
    )

    raw_materials = models.ManyToManyField(
        "raw_materials.RawMaterial",
        verbose_name="Materias primas",
        through="MaterialSaleRelation",
        through_fields=("sale", "raw_material")
    )

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"

    def __str__(self):
        return '%s %d' % (self._meta.verbose_name, self.pk)

    # def get_absolute_url(self):
    #     return reverse("Sale_detail", kwargs={"pk": self.pk})


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

    class Meta:
        pass
