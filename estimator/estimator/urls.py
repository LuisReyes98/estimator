"""
Urls del sistema
"""
# from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
