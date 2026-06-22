from django.urls import path

from . import views

app_name='credits'

urlpatterns=[
    path('', views.credit_list, name='credit_list'),
    path('create/', views.create_credit, name='create_credit'),
    path('payment/add/', views.create_credit_payment, name='create_credit_payment'),
    path("credit/remboursement/", views.credit_remboursement, name="credit_remboursement")
]