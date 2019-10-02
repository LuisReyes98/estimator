# from django.shortcuts import render
from django.views.generic import FormView, TemplateView
from .forms import SelectPredictionForm
from django.urls import reverse_lazy
# from django.shortcuts import redirect
# Create your views here.


class PredictionFormView(FormView):
    template_name = "predictions/select_prediction.html"
    success_url = reverse_lazy("sales:calendar")
    form_class = SelectPredictionForm

    def get_form_kwargs(self):
        form_kwargs = super(PredictionFormView, self).get_form_kwargs()

        form_kwargs['user'] = self.request.user
        return form_kwargs
