# Django
from django.urls import path
from . import views

urlpatterns = [
    path(
        route='generate/',
        view=views.PredictionFormView.as_view(),
        name="generate"
    ),
]
