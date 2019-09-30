# Django
from django.urls import path

# Views
from sales import views, sale_files_views


urlpatterns = [
    path(
        route='calendar/',
        view=views.CalendarView.as_view(),
        name='calendar'
    ),
    path(
        route='new_sale/',
        view=views.SaleCreateView.as_view(),
        name='new_sale'
    ),
    path(
        route='sales_list/',
        view=views.SaleListView.as_view(),
        name='sales_list'
    ),
    path(
        route='<int:pk>/',
        view=views.SaleDetailView.as_view(),
        name='sale'
    ),
    path(
        route='update/<int:pk>/',
        view=views.SaleUpdateView.as_view(),
        name='update_sale'
    ),
    path(
        route="delete/<int:pk>/",
        view=views.SaleDeleteView.as_view(),
        name="delete_sale"
    ),
    path(
        route="upload/",
        view=sale_files_views.SaleUploadFileView.as_view(),
        name="upload_file"
    )
    ,
    path(
        route="upload/success/",
        view=sale_files_views.SaleUploadedFileView.as_view(),
        name="uploaded_file"
    )
]
