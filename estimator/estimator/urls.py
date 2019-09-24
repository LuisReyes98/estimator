"""estimator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path(
        route='',
        view=views.HomeView.as_view(),
        name='home'
    ),
    path(
        'sales/',
        include(
            ('sales.urls', 'sales'),
            namespace='sales')
        ),
    path(
        'raw_materials/',
        include(
            ('raw_materials.urls', 'raw_materials'),
            namespace='raw_materials'
        )
    ),
    path(
        'users/',
        include(
            ('users.urls', 'users'),
            namespace="users"
        )
    ),
    path(
        'apiv1/',
        include(
            ('api.urls', 'api'),
            namespace="api"
        )
    ),
    path(
        'settings/',
        include(
            ('configurations.urls', 'configurations'),
            namespace="settings"
        )
    ),
]
