from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)
from raw_materials.models import Provider
from django.urls import reverse_lazy
from .forms import ProviderForm
from django.shortcuts import redirect


class ProviderListView(LoginRequiredMixin, ListView):
    """Vista listado de todos los proveedores"""
    model = Provider
    template_name = "providers/providers_list.html"

    def get_queryset(self):
        new_context = Provider.objects.filter(
            company=self.request.user.company.pk,
        )
        return new_context

    def get_context_data(self, **kwargs):
        """User and profile to context"""
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["current_page"] = "providers"
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
        context["current_page"] = "providers"
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

    def get_context_data(self, **kwargs):
        """User and profile to context"""
        context = super().get_context_data(**kwargs)
        context["current_page"] = "providers"
        return context


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
        context["current_page"] = "providers"

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
