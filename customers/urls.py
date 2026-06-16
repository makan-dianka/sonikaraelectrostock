from django.urls import path

from . import views


app_name = 'customers'

urlpatterns = [
    path('', views.customer_list, name='list'),
    path('create/', views.customer_create, name='create'),
    path('update/<int:pk>', views.update_customer, name='update'),

    path('<int:pk>/delete/', views.delete_customer, name="delete"),
]