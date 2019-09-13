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
        route="update/<int:pk>/",
        view=views.ProviderUpdateView.as_view(),
        name="update_provider"
    ),
    path(
        route="delete/<int:pk>/",
        view=views.ProviderDeleteView.as_view(),
        name="delete_provider"
    )
]

raw_material_patterns = [
    path(
        route="",
        view=views.RawMaterialListView.as_view(),
        name="materials"
    ),
    path(
        route="new/",
        view=views.RawMaterialCreateView.as_view(),
        name="new_material"
    ),
    path(
        route="<int:pk>/",
        view=views.RawMaterialDetailView.as_view(),
        name="material"
    ),
    path(
        route="update/<int:pk>/",
        view=views.RawMaterialUpdateView.as_view(),
        name="update_material"
    ),
    path(
        route="delete/<int:pk>/",
        view=views.RawMaterialDeleteView.as_view(),
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
