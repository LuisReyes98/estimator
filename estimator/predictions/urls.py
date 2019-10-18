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
        route='result/',
        view=views.PredictionResultView.as_view(),
        name="result"
    ),
    path(
        route='prediction_list/',
        view=views.PredictionListView.as_view(),
        name="list"
    ),
    path(
        route='prediction/<int:pk>/',
        view=views.PredictionDetailView.as_view(),
        name="prediction"
    ),
]
