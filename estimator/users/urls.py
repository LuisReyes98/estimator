# Django
from django.urls import path

# Models
from users import views

urlpatterns = [
    path(
        route='login/',
        view=views.LoginView.as_view(),
        name='login'
    ),
    # path(
    #     route='login/?signed',
    #     view=views.LoginView.as_view(),
    #     name='login'
    # ),
    path(
        route='logout/',
        view=views.LogoutView.as_view(),
        name='logout'
    ),

    path(
        route='signup/',
        view=views.RegisterCompanyView.as_view(),
        name='signup',
    ),

    path(
        route='company_users_list/',
        view=views.CompanyUserListView.as_view(),
        name='company_users_list',
    ),

    path(
        route='company_users_new/',
        view=views.CompanyUserCreateView.as_view(),
        name='create_company_user',
    ),
]
