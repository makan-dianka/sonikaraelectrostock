from django.urls import path

from common.search import search_api

from . import views


app_name = 'suppliers'

urlpatterns = [
    path('', views.supplier_list, name='list'),
    path('create/', views.supplier_create, name='create'),
    path('update/<int:pk>', views.update_supplier, name='update_supplier'),

    path('<int:pk>/delete/', views.delete_supplier, name="delete"),

    path('api/supplier/search/', views.supplier_search_api, name='supplier_search_api'),
    path('api/supplier/create/', views.create_supplier_api, name='create_supplier_api'),

    path("search/<str:entity>/", search_api, name="search_api"),
]