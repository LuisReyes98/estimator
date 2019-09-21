# Django
from django.urls import path, include

# Materia prima
from . import raw_material_views as m_views
from . import provider_views as p_views

provider_patterns = [
    path(
        route='',
        view=p_views.ProviderListView.as_view(),
        name='providers'
    ),
    path(
        route='<int:pk>/',
        view=p_views.ProviderDetailView.as_view(),
        name='provider'
    ),
    path(
        route='new/',
        view=p_views.ProviderCreateView.as_view(),
        name='new_provider'
    ),
    path(
        route="update/<int:pk>/",
        view=p_views.ProviderUpdateView.as_view(),
        name="update_provider"
    ),
    path(
        route="delete/<int:pk>/",
        view=p_views.ProviderDeleteView.as_view(),
        name="delete_provider"
    )
]

raw_material_patterns = [
    path(
        route="",
        view=m_views.RawMaterialListView.as_view(),
        name="materials"
    ),
    path(
        route="new/",
        view=m_views.RawMaterialCreateView.as_view(),
        name="new_material"
    ),
    path(
        route="<int:pk>/",
        view=m_views.RawMaterialDetailView.as_view(),
        name="material"
    ),
    path(
        route="update/<int:pk>/",
        view=m_views.RawMaterialUpdateView.as_view(),
        name="update_material"
    ),
    path(
        route="delete/<int:pk>/",
        view=m_views.RawMaterialDeleteView.as_view(),
        name="delete_material"
    )
]

urlpatterns = [
    path(
        "providers/",
        include((provider_patterns), namespace=''),
    ),
    path(
        "materials/",
        include((raw_material_patterns), namespace=''),
    ),
]
