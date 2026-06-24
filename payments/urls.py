from django.urls import path

from . import views

app_name='payments'

urlpatterns=[
    path('create/', views.create_payment, name='create'),
    path('', views.payment_list, name='list'),
]