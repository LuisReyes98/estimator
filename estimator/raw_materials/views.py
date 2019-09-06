from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)
from raw_materials.models import Provider, RawMaterial
from django.urls import reverse_lazy
from .forms import ProviderForm, RawMaterialForm
from django.shortcuts import redirect
# Create your views here.


class ProviderListView(LoginRequiredMixin, ListView):
    """Vista listado de todos los proveedores"""
    model = Provider
    template_name = "providers/providers_list.html"

    def get_queryset(self):
        new_context = Provider.objects.filter(
            company=self.request.user.company,
        )
        return new_context

    def get_context_data(self, **kwargs):
        """User and profile to context"""
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["company"] = self.request.user.company
        return context


class ProviderCreateView(LoginRequiredMixin, CreateView):
    model = Provider
    template_name = "providers/provider_form.html"
    success_url = reverse_lazy('raw_materials:providers')
    form_class = ProviderForm

    def get_context_data(self, **kwargs):
        """User and profile to context"""
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["company"] = self.request.user.company
        context["form_url"] = reverse_lazy('raw_materials:new_provider')
        return context


class ProviderDetailView(LoginRequiredMixin, DetailView):
    model = Provider
    template_name = "providers/provider_detail.html"

    def get(self, request, *args, **kwargs):
        if self.get_object().company.pk != self.request.user.company.pk:
            return redirect('raw_materials:providers')
        return super().get(request, *args, **kwargs)


class ProviderUpdateView(LoginRequiredMixin, UpdateView):
    model = Provider
    template_name = "providers/provider_form.html"
    form_class = ProviderForm

    def get(self, request, *args, **kwargs):
        if self.get_object().company.pk != self.request.user.company.pk:
            return redirect('raw_materials:providers')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """User and profile to context"""
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["company"] = self.request.user.company
        context["form_url"] = reverse_lazy(
            'raw_materials:update_provider',
            args=[self.object.pk]
        )
        context["editing"] = True
        return context


class ProviderDeleteView(LoginRequiredMixin, DeleteView):
    model = Provider
    template_name = "providers/provider_delete.html"
    success_url = reverse_lazy('raw_materials:providers')

    def get(self, request, *args, **kwargs):
        if self.get_object().company.pk != self.request.user.company.pk:
            return redirect('raw_materials:providers')
        return super().get(request, *args, **kwargs)


class RawMaterialListView(ListView):
    model = RawMaterial
    template_name = "raw_materials/raw_materials_list.html"

    def get_queryset(self):
        new_context = RawMaterial.objects.filter(
            company=self.request.user.company,
        )
        return new_context


class RawMaterialCreateView(CreateView):
    model = RawMaterial
    template_name = "raw_materials/raw_material_form.html"
    success_url = reverse_lazy('raw_materials:materials')
    form_class = RawMaterialForm

    def get_context_data(self, **kwargs):
        """User and profile to context"""
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["company"] = self.request.user.company
        context["form_url"] = reverse_lazy('raw_materials:new_material')
        return context


class RawMaterialDetailView(DetailView):
    model = RawMaterial
    template_name = ".html"


class RawMaterialUpdateView(UpdateView):
    model = RawMaterial
    template_name = ".html"


class RawMaterialDeleteView(DeleteView):
    model = RawMaterial
    template_name = ".html"
