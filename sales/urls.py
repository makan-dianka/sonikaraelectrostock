from django.urls import path

from . import views

app_name='sales'

urlpatterns=[
    path('', views.sale_list, name='list'),
    path('create/', views.create_sale, name='create'),
    path('<int:pk>/validate/', views.validate_sale_view, name='validate'),
    path('<int:pk>/cancel/', views.cancel_sale_view, name='cancel'),
    path('<int:pk>/update/', views.update_sale, name='update'),

    path("invoice/<int:pk>/", views.print_invoice, name="print_invoice",),
]