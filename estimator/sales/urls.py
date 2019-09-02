# Django
from django.urls import path

# Models
from sales import views

urlpatterns = [
    path(
        route='calendar/',
        view=views.CalendarView.as_view(),
        name='calendar'
    ),
]
