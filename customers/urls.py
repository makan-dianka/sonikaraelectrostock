from django.urls import path

from . import views


app_name = 'customers'

urlpatterns = [
    path('', views.customer_list, name='list'),
    path('create/', views.customer_create, name='create'),
    path('update/<int:pk>', views.update_customer, name='update'),

    path('<int:pk>/delete/', views.delete_customer, name="delete"),

    path('api/customer/search/', views.customer_search_api, name='customer_search_api'),
    path('api/customer/create/', views.create_customer_api, name='create_customer_api'),
]