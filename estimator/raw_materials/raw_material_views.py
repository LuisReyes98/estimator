from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)
from raw_materials.models import RawMaterial
from django.urls import reverse_lazy
from .forms import RawMaterialForm
from django.shortcuts import redirect


class RawMaterialListView(LoginRequiredMixin, ListView):
    model = RawMaterial
    template_name = "raw_materials/raw_materials_list.html"

    def get_queryset(self):
        new_context = RawMaterial.objects.filter(
            company=self.request.user.safe_company.pk,
        )
        return new_context

    def get_context_data(self, **kwargs):
        """Contexto de lista de materia prima"""
        context = super().get_context_data(**kwargs)
        context["current_page"] = "materials"
        return context


class RawMaterialCreateView(LoginRequiredMixin, CreateView):
    model = RawMaterial
    template_name = "raw_materials/raw_material_form.html"
    success_url = reverse_lazy('raw_materials:materials')
    form_class = RawMaterialForm

    def get_form_kwargs(self):
        form_kwargs = super(RawMaterialCreateView, self).get_form_kwargs()

        form_kwargs['user'] = self.request.user

        return form_kwargs

    def get_context_data(self, **kwargs):
        """User and profile to context"""
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["current_page"] = "materials"
        context["company"] = self.request.user.safe_company
        context["form_url"] = reverse_lazy('raw_materials:new_material')
        return context


class RawMaterialDetailView(LoginRequiredMixin, DetailView):
    model = RawMaterial
    template_name = "raw_materials/raw_material_detail.html"

    def get(self, request, *args, **kwargs):
        if self.get_object().company.pk != self.request.user.safe_company.pk:
            return redirect('raw_materials:materials')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Contexto de detalle de materia prima"""
        context = super().get_context_data(**kwargs)
        context["current_page"] = "materials"
        return context


class RawMaterialUpdateView(LoginRequiredMixin, UpdateView):
    model = RawMaterial
    template_name = "raw_materials/raw_material_form.html"
    success_url = reverse_lazy('raw_materials:materials')
    form_class = RawMaterialForm

    def get(self, request, *args, **kwargs):
        if self.get_object().company.pk != self.request.user.safe_company.pk:
            return redirect('raw_materials:materials')
        return super().get(request, *args, **kwargs)

    def get_form_kwargs(self):
        form_kwargs = super(RawMaterialUpdateView, self).get_form_kwargs()
        form_kwargs['user'] = self.request.user

        return form_kwargs

    def get_context_data(self, **kwargs):
        """Usuarios, compañia, y url al formulario"""
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["company"] = self.request.user.safe_company
        context["form_url"] = reverse_lazy(
            'raw_materials:update_material',
            args=[self.object.pk]
        )
        context["editing"] = True
        context["current_page"] = "materials"
        return context


class RawMaterialDeleteView(LoginRequiredMixin, DeleteView):
    model = RawMaterial
    template_name = "raw_materials/raw_material_delete.html"
    success_url = reverse_lazy('raw_materials:materials')

    def get(self, request, *args, **kwargs):
        if self.get_object().company.pk != self.request.user.safe_company.pk:
            return redirect('raw_materials:materials')
        return super().get(request, *args, **kwargs)
