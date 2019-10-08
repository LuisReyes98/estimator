
# Django
from django.urls import path, include

# Models
from . import views

users_urlpatterns = [
    path(
        route='settings/',
        view=views.TemplateView.as_view(),
        name='settings',
    ),
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
    path(
        route='<int:pk>/',
        view=views.CompanyUserDetailView.as_view(),
        name='company_user'
    ),
    path(
        route="update/<int:pk>/",
        view=views.CompanyUserUpdateView.as_view(),
        name="update_company_user"
    ),
    path(
        route="update/<int:pk>/",
        view=views.CompanyUserUpdateView.as_view(),
        name="update_company_user"
    ),
    path(
        route="update/password/<int:pk>/",
        view=views.CompanyUserUpdatePasswordView.as_view(),
        name="update_password_company_user"
    ),
    path(
        route="delete/<int:pk>/",
        view=views.CompanyUserDeleteView.as_view(),
        name="delete_company_user"
    ),
    path(
        route="update/current/",
        view=views.CurrentUserUpdateView.as_view(),
        name="update_current_user"
    ),
    path(
        route="update/currency/",
        view=views.CurrencyUpdateView.as_view(),
        name="update_currency"
    ),
]

urlpatterns = [
    path(
        "company_users/",
        include((users_urlpatterns), namespace=''),
    ),
]