from django.shortcuts import render
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from users.models import CompanyUser
from .forms import CompanyUserForm
# Create your views here.


class CompanyUserListView(LoginRequiredMixin, ListView):
    model = CompanyUser
    template_name = "settings/company_users_list.html"

    def get_queryset(self):
        new_context = CompanyUser.objects.filter(
            company=self.request.user.company.pk,
        )
        return new_context

    def get_context_data(self, **kwargs):
        """Contexto de lista de materia prima"""
        context = super().get_context_data(**kwargs)
        context["current_page"] = "company_users"
        return context


class CompanyUserCreateView(LoginRequiredMixin, CreateView):
    model = CompanyUser
    template_name = "settings/company_users_form.html"
    success_url = reverse_lazy('settings:company_users_list')
    form_class = CompanyUserForm

    # def get_form_kwargs(self):
    #     form_kwargs = super(CompanyUserCreateView, self).get_form_kwargs()

    #     form_kwargs['creator_company'] = self.request.user.company.pk

    #     return form_kwargs

    def get_context_data(self, **kwargs):
        """User and profile to context"""
        context = super().get_context_data(**kwargs)
        context["current_page"] = "company_users"
        context["company"] = self.request.user.company
        context["form_url"] = reverse_lazy('settings:create_company_user')
        return context


class CompanyUserDetailView(LoginRequiredMixin, DetailView):
    model = CompanyUser
    template_name = ".html"


class CompanyUserDeleteView(LoginRequiredMixin, DeleteView):
    model = CompanyUser
    template_name = ".html"


"""
def get_form_kwargs(self):
        form_kwargs = super(RawMaterialCreateView, self).get_form_kwargs()

        form_kwargs['creator_company'] = self.request.user.company

        return form_kwargs

"""