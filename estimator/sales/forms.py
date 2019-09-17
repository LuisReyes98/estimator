from django import forms
from .models import Sale, MaterialSaleRelation
from raw_materials.models import RawMaterial

class SaleForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(SaleForm, self).__init__(*args, **kwargs)

        self.fields['raw_materials'].queryset = RawMaterial.objects.filter(
            company=user.company.pk,
        )

    class Meta:
        model = Sale
        fields = (
            "total_cost_dollar",
            "total_cost_local",
            "company",
            "company_user",
            "raw_materials"
        )
