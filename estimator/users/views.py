from django.shortcuts import render
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, FormView
# Create your views here.


class LoginView(auth_views.LoginView):
    """Vista de iniciar sesion """
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get(self, request, *args, **kwargs):
        """añadiendo variables al contexto en get"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Iniciar Sesion"
        return self.render_to_response(context)


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """ Vista de cerrar sesion , logica sin html """


class RegisterCompany(FormView):
    """Vista de registro de una nueva comap"""
