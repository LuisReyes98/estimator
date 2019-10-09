from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from users.models import CompanyUser, Company
from .forms import CompanyUserForm, CompanyUserFormFields, CompanyUserFormPassword, CurrentUserFormFields, CurrencyFormFields, CurrentUserFormPassword
from django.contrib.auth.views import PasswordChangeView
# Create your views here.

class TemplateView(TemplateView):
    template_name = "settings/settings.html"


class CompanyUserListView(LoginRequiredMixin, ListView):
    model = CompanyUser
    template_name = "settings/company_users_list.html"

    def get_queryset(self):
        new_context = CompanyUser.objects.filter(
            company=self.request.user.company.pk,
        )
        return new_context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_page"] = "company_users"
        return context


class CompanyUserCreateView(LoginRequiredMixin, CreateView):
    model = CompanyUser
    template_name = "settings/company_users_form.html"
    success_url = reverse_lazy('settings:company_users_list')
    form_class = CompanyUserForm

    def get_form_kwargs(self):
        form_kwargs = super(CompanyUserCreateView, self).get_form_kwargs()

        if self.request.user.is_superuser:
            form_kwargs['creator_company'] = self.request.user.company
        else:
            form_kwargs['creator_company'] = self.request.user.companyuser.company


        return form_kwargs

    def get_context_data(self, **kwargs):
        """User and profile to context"""
        context = super().get_context_data(**kwargs)
        context["current_page"] = "company_users"
        # context["company"] = self.request.user.company
        context["form_url"] = reverse_lazy('settings:create_company_user')
        return context


class CompanyUserDetailView(LoginRequiredMixin, DetailView):
    model = CompanyUser
    template_name = "settings/company_users_detail.html"

    def get(self, request, *args, **kwargs):
        if self.get_object().company.pk != self.request.user.company.pk:
            return redirect('settings:company_users_list')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CompanyUserUpdateView(LoginRequiredMixin, UpdateView):
    model = CompanyUser
    template_name = "settings/company_users_form.html"
    success_url = reverse_lazy('settings:company_users_list')
    form_class = CompanyUserForm

    def get_form_kwargs(self):
        form_kwargs = super(CompanyUserUpdateView, self).get_form_kwargs()

        if self.request.user.is_superuser:
            form_kwargs['creator_company'] = self.request.user.company
        else:
            form_kwargs['creator_company'] = self.request.user.companyuser.company
        return form_kwargs

    def get_context_data(self, **kwargs):
        """User and profile to context"""
        context = super().get_context_data(**kwargs)
        context["current_page"] = "company_users"
        context["company"] = self.request.user.company
        context["form_url"] = reverse_lazy(
            'settings:update_company_user',
            args=[self.object.pk]
        )
        context["editing"] = True
        return context

class CompanyUserUpdatePasswordView(LoginRequiredMixin, UpdateView):
    model = CompanyUser
    template_name = "settings/company_users_form_pass.html"
    success_url = reverse_lazy('settings:company_users_list')
    form_class = CompanyUserFormPassword

    def get_form_kwargs(self):
        form_kwargs = super(CompanyUserUpdatePasswordView, self).get_form_kwargs()

        if self.request.user.is_superuser:
            form_kwargs['creator_company'] = self.request.user.company
        else:
            form_kwargs['creator_company'] = self.request.user.companyuser.company
        return form_kwargs

    def get_context_data(self, **kwargs):
        """User and profile to context"""
        context = super().get_context_data(**kwargs)
        context["current_page"] = "company_users"
        context["company"] = self.request.user.company
        context["form_url"] = reverse_lazy(
            'settings:update_password_company_user',
            args=[self.object.pk]
        )
        context["editing"] = True
        return context

class CompanyUserUpdateView(LoginRequiredMixin, UpdateView):
    model = CompanyUser
    template_name = "settings/company_users_form_fields.html"
    success_url = reverse_lazy('settings:company_users_list')
    form_class = CompanyUserFormFields

    def get_form_kwargs(self):
        form_kwargs = super(CompanyUserUpdateView, self).get_form_kwargs()

        if self.request.user.is_superuser:
            form_kwargs['creator_company'] = self.request.user.company
        else:
            form_kwargs['creator_company'] = self.request.user.companyuser.company
        return form_kwargs

    def get_context_data(self, **kwargs):
        """User and profile to context"""
        context = super().get_context_data(**kwargs)
        context["current_page"] = "company_users"
        context["company"] = self.request.user.company
        context["form_url"] = reverse_lazy(
            'settings:update_company_user',
            args=[self.object.pk]
        )
        context["editing"] = True
        return context

class CompanyUserDeleteView(LoginRequiredMixin, DeleteView):
    model = CompanyUser
    template_name = "settings/company_users_delete.html"
    success_url = reverse_lazy('settings:company_users_list')

    def get(self, request, *args, **kwargs):
        if self.get_object().company.pk != self.request.user.company.pk:
            return redirect('settings:company_users_list')
        return super().get(request, *args, **kwargs)

class CurrentUserUpdateView(LoginRequiredMixin, UpdateView):
    model = CompanyUser
    template_name = "settings/current_users_form.html"
    success_url = reverse_lazy('settings:settings')
    form_class = CurrentUserFormFields

    # def get_form_kwargs(self):
    #     form_kwargs = super(CompanyUserUpdateView, self).get_form_kwargs()

    #     if self.request.user.is_superuser:
    #         form_kwargs['creator_company'] = self.request.user.company
    #     else:
    #         form_kwargs['creator_company'] = self.request.user.companyuser.company
    #     return form_kwargs

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        """User and profile to context"""
        context = super().get_context_data(**kwargs)
        context["current_page"] = "company_users"
        context["company"] = self.request.user.company
        context["form_url"] = reverse_lazy(
            'settings:update_current_user'
        )
        context["editing"] = True
        return context

class CurrentUserUpdatePasswordView(PasswordChangeView):
    template_name = "settings/current_users_form_pass.html"
    success_url = reverse_lazy('settings:settings')


# class PasswordChangeView(LoginRequiredMixin, UpdateView):
#     model = CompanyUser
#     template_name = "settings/current_users_form_pass.html"
#     success_url = reverse_lazy('settings:settings')
#     form_class = CurrentUserFormPassword

#     def get_context_data(self, **kwargs):
#         """User and profile to context"""
#         context = super().get_context_data(**kwargs)
#         context["current_page"] = "company_users"
#         context["company"] = self.request.user.company
#         context["form_url"] = reverse_lazy(
#             'settings:update_password_current_user'
#         )
#         context["editing"] = True
#         return context

class CurrencyUpdateView(UpdateView):
    model = Company
    template_name = "settings/update_currency.html"
    success_url = reverse_lazy('settings:settings')
    form_class = CurrencyFormFields

    # def get_form_kwargs(self):
    #     form_kwargs = super(CompanyUserUpdateView, self).get_form_kwargs()

    #     if self.request.user.is_superuser:
    #         form_kwargs['creator_company'] = self.request.user.company
    #     else:
    #         form_kwargs['creator_company'] = self.request.user.companyuser.company
    #     return form_kwargs

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        """User and profile to context"""
        context = super().get_context_data(**kwargs)
        context["current_page"] = "company_users"
        context["company"] = self.request.user.company
        context["form_url"] = reverse_lazy(
            'settings:update_currency'
        )
        context["editing"] = True
        return context


"""
def get_form_kwargs(self):
        form_kwargs = super(RawMaterialCreateView, self).get_form_kwargs()

        form_kwargs['creator_company'] = self.request.user.company

        return form_kwargs

"""