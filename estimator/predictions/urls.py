# Django
from django.urls import path
from . import views

urlpatterns = [
    path(
        route='generate/',
        view=views.PredictionFormView.as_view(),
        name="generate"
    ),
    path(
        route='result',
        view=views.PredictionResultView.as_view(),
        name="result"
    ),
]
