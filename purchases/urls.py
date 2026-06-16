from django.urls import path

from . import views


app_name = 'purchases'

urlpatterns = [
    path('', views.purchase_list, name='list'),
    path('create/', views.purchase_create, name='create'),
    path('<int:pk>/status/<str:status>/', views.update_status, name='update_status'),
]