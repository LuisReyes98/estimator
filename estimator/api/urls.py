# Django
from django.urls import path

# Models
from api import views

urlpatterns = [
    path(
        route='session/<str:session_var>/',
        view=views.SessionVariablesAPI.as_view(),
        name='session_api'
    ),
]
