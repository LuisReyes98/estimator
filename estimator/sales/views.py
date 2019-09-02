from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
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
