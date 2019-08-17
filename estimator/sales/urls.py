# Django
from django.urls import path

# Models
from sales import views

urlpatterns = [
    path(
        route='',
        view=views.HomeView.as_view(),
        name='home'
    ),
    path(
        route='test/',
        view=views.VistaTest.as_view(),
        name='test'
    ),
]
