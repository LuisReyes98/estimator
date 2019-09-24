from django.shortcuts import render
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from users.forms import CreateCompanyForm
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)
from .models import CompanyUser
from .forms import CreateCompanyUserForm

# Create your views here.


class LoginView(auth_views.LoginView):
    """Vista de iniciar sesion """
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        """Agregando variables al contexto"""
        context = super().get_context_data(**kwargs)

        context["title"] = "Iniciar Sesión"

        return context

    def get(self, request, *args, **kwargs):
        """añadiendo variables al contexto en get"""
        context = self.get_context_data(**kwargs)
        if request.GET.get("signed"):
            context["signed"] = True
        if request.GET.get("next"):
            context["next"] = request.GET.get("next")

        return self.render_to_response(context)


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """ Vista de cerrar sesion , logica sin html """


class RegisterCompanyView(FormView):
    """Vista de registro de una nueva comap"""

    template_name = "users/signup.html"

    form_class = CreateCompanyForm

    success_url = '/users/login/?signed=True'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Agregando variables al contexto"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Registrarse"
        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)

class CompanyUserListView(LoginRequiredMixin, ListView):
    model = CompanyUser
    template_name = "users/company_users_list.html"

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
    template_name = "users/company_users_form.html"
    success_url = reverse_lazy('home')
    form_class = CreateCompanyUserForm

    # def get_form_kwargs(self):
    #     form_kwargs = super(CompanyUserCreateView, self).get_form_kwargs()

    #     form_kwargs['creator_company'] = self.request.user.company.pk

    #     return form_kwargs

    def get_context_data(self, **kwargs):
        """User and profile to context"""
        context = super().get_context_data(**kwargs)
        context["current_page"] = "company_users"
        context["company"] = self.request.user.company
        context["form_url"] = reverse_lazy('users:create_company_user')
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