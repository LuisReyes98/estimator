from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.

class GraphicsView(TemplateView):
    template_name = "graphics/graphics.html"

    def get_context_data(self, **kwargs):
        """Añadiendo variables al contexto """
        context = super().get_context_data(**kwargs)

        return context
