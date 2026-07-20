from django.urls import path

from . import views
from common.search import search_api


app_name = 'purchases'

urlpatterns = [
    path('', views.purchase_list, name='list'),
    path('create/', views.purchase_create, name='create'),
    path('<int:pk>/status/<str:status>/', views.update_status, name='update_status'),
    path('<int:pk>/update/', views.update_purchase, name='update'),
    path("search/<str:entity>/", search_api, name="search_api"),

    path("order/<int:pk>/", views.print_purchase, name="print_purchase",),
]