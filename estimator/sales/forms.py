from django import forms
from .models import Sale, MaterialSaleRelation


class SaleForm(forms.ModelForm):

    class Meta:
        model = Sale
        fields = (
            "total_cost_dollar",
            "total_cost_local",
            "company",
            "company_user",
            "raw_materials"
        )
