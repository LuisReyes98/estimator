# Django
from django.urls import path

# Models
from users import views

urlpatterns = [
    path(
        route='login/',
        view=views.LoginView.as_view(),
        name='login'
    ),

    path(
        route='logout/',
        view=views.LogoutView.as_view(),
        name='logout'
    ),

    path(
        route='signup/',
        view=views.RegisterCompany.as_view(),
        name='signup',
    ),
]
