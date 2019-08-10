from django.shortcuts import render
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class LoginView(auth_views.LoginView):
    """Vista de iniciar sesion """
    template_name = 'users/login.html'
    redirect_authenticated_user = True


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """ Vista de cerrar sesion , logica sin html """
