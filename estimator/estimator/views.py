from django.views.generic import DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from predictions.models import PredictionSale


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
    # context_object_name = 'estimation'

    def get_context_data(self, **kwargs):
        """Añadiendo variables al contexto """
        context = super().get_context_data(**kwargs)
        # context["title"] = "Bienvenido"
        try:
            context['prediction'] = PredictionSale.objects.filter(
                company=self.request.user.safe_company
            ).latest('created')
        except Exception:
            context['prediction'] = None

        context["user"] = self.request.user
        context["current_page"] = "home"

        return context
