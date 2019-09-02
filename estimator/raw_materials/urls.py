# Django
from django.urls import path, include

# Materia prima
from raw_materials import views

provider_patterns = [
    path(
        route='',
        view=views.ProviderListView.as_view(),
        name='providers'
    ),
    path(
        route='<int:pk>/',
        view=views.ProviderDetailView.as_view(),
        name='provider'
    ),
    path(
        route='new/',
        view=views.ProviderCreateView.as_view(),
        name='new_provider'
    ),
    path(
        "update/<int:pk>/",
        views.ProviderUpdateView.as_view(),
        name="update_provider"
    ),
    path(
        "delete/<int:pk>/",
        views.ProviderDeleteView.as_view(),
        name="delete_provider"
    )
]

urlpatterns = [
    path(
        "providers/",
        include((provider_patterns), namespace=''),
    ),
]
