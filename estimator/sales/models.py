from django.db import models
from django.utils.translation import ugettext_lazy as translate
from estimator.mixins import TimeStampFields
# Modelos para las ventas


class Sale(TimeStampFields):
    """ Venta de un grupo de productos """
    # campos propios

    total_cost_dollar = models.FloatField(
        translate("Total sale cost in Dollars")
    )

    total_cost_local = models.FloatField(
        translate("Total sale cost in the local coin"),
    )

    # Referencias
    company = models.ForeignKey(  # Compañia a la que pertenece
        'users.Company',
        on_delete=models.SET_NULL,
        parent_link=True,
        blank=True,
        null=True,
    )

    company_user = models.ForeignKey(  # Compañia a la que pertenece
        'users.CompanyUser',
        on_delete=models.SET_NULL,
        parent_link=True,
        blank=True,
        null=True,
    )

    raw_materials = models.ManyToManyField(
        "raw_materials.RawMaterial",
        verbose_name=translate("Raw Materials"),
        through="MaterialSaleRelation",
        through_fields=("sale", "raw_material")
    )

    class Meta:
        verbose_name = translate("Sale")
        verbose_name_plural = translate("Sales")

    def __str__(self):
        return '%s %d' % (self._meta.verbose_name, self.pk)

    # def get_absolute_url(self):
    #     return reverse("Sale_detail", kwargs={"pk": self.pk})


class MaterialSaleRelation(TimeStampFields):
    """ Relacion entre un venta y materia prima para lograr almacenar
    informacion extra """

    # Campos propios
    amount = models.PositiveIntegerField(
        translate("Amount")
    )

    cost_dollar = models.FloatField(
        translate("Cost in Dollars")
    )

    cost_local = models.FloatField(
        translate("Cost in the local coin"),
    )

    # Referencias
    raw_material = models.ForeignKey(
        "raw_materials.RawMaterial",
        verbose_name=translate("Raw Material"),
        null=True,
        on_delete=models.SET_NULL,
        related_name="sold_ocassions",
        # nombre con el cual se accede a este
        # modelo desde el modelo materia prima (raw material)
    )

    sale = models.ForeignKey(
        "Sale",
        verbose_name=translate("Sale"),
        on_delete=models.CASCADE,
        related_name="sold_materials",
    )

    class Meta:
        pass
