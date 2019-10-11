"""
Urls del sistema
"""
# from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# import estimations
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
        'predictions/',
        include(
            ('predictions.urls', 'predictions'),
            namespace="predictions"
        )
    ),
    path(
        'settings/',
        include(
            ('configurations.urls', 'configurations'),
            namespace="settings"
        )
    ),
    path(
        'graphics/',
        include(
            ('graphics_statistics.urls', 'graphics_statistics'),
            namespace="graphics"
        )
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
