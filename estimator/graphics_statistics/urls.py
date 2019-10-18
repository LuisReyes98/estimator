from django.urls import path
from . import views

urlpatterns = [
    path(
        route='',
        view=views.GraphicsView.as_view(),
        name="graphs"
    ),
    # path(
    #     route='report/',
    #     view=views.ReportsView.as_view(),
    #     name="report"
    # ),
]