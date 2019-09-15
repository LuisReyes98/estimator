from django.shortcuts import render
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from users.forms import CreateCompanyForm

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
