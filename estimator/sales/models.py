from django.db import models
from django.utils.translation import ugettext_lazy as translate
from users.models import Company, CompanyUser
# Modelos para las ventas


class Sale(models.Model):
    """ Venta de un grupo de productos """
    # Referencias
    company = models.ForeignKey(  # Compañia a la que pertenece
        Company,
        on_delete=models.SET_NULL,
        parent_link=True,
        blank=True,
        null=True,
    )

    company_user = models.ForeignKey(  # Compañia a la que pertenece
        CompanyUser,
        on_delete=models.SET_NULL,
        parent_link=True,
        blank=True,
        null=True,
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = translate("Sale")
        verbose_name_plural = translate("Sales")

    def __str__(self):
        return translate("Sale ") + self.pk

    # def get_absolute_url(self):
    #     return reverse("Sale_detail", kwargs={"pk": self.pk})
