from django.shortcuts import render
from django.views.generic import DetailView, TemplateView
# Create your views here.


class HomeView(TemplateView):
    template_name = 'home.html'
    # context_object_name = 'estimation'
