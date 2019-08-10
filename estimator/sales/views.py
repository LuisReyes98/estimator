from django.shortcuts import render
from django.views.generic import DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
    # context_object_name = 'estimation'

    def get_context_data(self, **kwargs):
        """Añadiendo variables al contexto """
        context = super().get_context_data(**kwargs)
        # context["user"] = self.request.user

        return context

    def get(self, request, *args, **kwargs):
        """añadiendo variables al contexto en get"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Bienvenido"
        context["user"] = self.request.user

        return self.render_to_response(context)
