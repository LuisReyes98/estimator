from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)
from raw_materials.models import Provider
# Create your views here.


class ProviderListView(LoginRequiredMixin, ListView):
    """Vista listado de todos los proveedores"""
    model = Provider
    template_name = "provider/provider_list.html"


class ProviderCreateView(LoginRequiredMixin, CreateView):
    model = Provider
    template_name = "provider/provider_form.html"
    fields = ['name', 'company']


class ProviderDetailView(LoginRequiredMixin, DetailView):
    model = Provider
    template_name = "provider/provider_detail.html"


class ProviderUpdateView(LoginRequiredMixin, UpdateView):
    model = Provider
    template_name = "provider/provider_form.html"


class ProviderDeleteView(LoginRequiredMixin, DeleteView):
    model = Provider
    template_name = "provider/provider_list.html"
