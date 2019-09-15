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
    path(
        route='new_sale/',
        view=views.SaleCreateView.as_view(),
        name='new_sale'
    ),
]
