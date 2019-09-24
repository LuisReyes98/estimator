
# Django
from django.urls import path, include

# Models
from . import views

users_urlpatterns = [
    path(
        route='list/',
        view=views.CompanyUserListView.as_view(),
        name='company_users_list',
    ),

    path(
        route='new/',
        view=views.CompanyUserCreateView.as_view(),
        name='create_company_user',
    ),
]

urlpatterns = [
    path(
        "company_users/",
        include((users_urlpatterns), namespace=''),
    ),
]