from django.shortcuts import render
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)
from raw_materials.models import Provider
# Create your views here.


class ProviderListView(ListView):
    """Vista listado de todos los proveedores"""
    model = Provider
    template_name = "provider/provider_list.html"


class ProviderCreateView(CreateView):

    model = Provider
    template_name = "provider/provider_form.html"


class ProviderDetailView(DetailView):
    model = Provider
    template_name = "provider/provider_detail.html"


class ProviderUpdateView(UpdateView):
    model = Provider
    template_name = "provider/provider_form.html"


class ProviderDeleteView(DeleteView):
    model = Provider
    template_name = "provider/provider_list.html"
