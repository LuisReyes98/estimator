from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.

class GraphicsView(TemplateView):
    template_name = "graphics/graphics.html"
