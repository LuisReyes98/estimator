from django.views.generic import TemplateView
from .models import Sale
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)
from datetime import datetime, timedelta
from sales.objects import Prediction
# Create your views here.


class CalendarView(LoginRequiredMixin, TemplateView):
    template_name = "sales/calendar.html"

    def exampleDates(self):
        now = datetime.now()
        some_dates = []

        for i in range(10):
            some_dates.append(
                Prediction(
                    date=(now - timedelta(days=i)).strftime("%m/%d/%Y"),
                    pk=i,
                ).__dict__
            )

        return some_dates

    def get(self, request, *args, **kwargs):

        """añadiendo variables al contexto en get"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Calendario"
        context["user"] = self.request.user

        context["predictions"] = self.exampleDates()

        return self.render_to_response(context)


class SaleDetailView(DetailView):
    model = Sale
    template_name = ".html"


class SaleListView(ListView):
    model = Sale
    template_name = ".html"


class SaleCreateView(CreateView):
    model = Sale
    template_name = ".html"


class SaleUpdateView(UpdateView):
    model = Sale
    template_name = ".html"


class SaleDeleteView(DeleteView):
    model = Sale
    template_name = ".html"
