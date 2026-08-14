from django.urls import path

from . import views

app_name='subscriptions'

urlpatterns=[
    path('expired/', views.expired, name='expired'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('subscription_plan/', views.subscription_plan, name='plan'),
    path('subscription_create/', views.subscription_create, name='subscription_create'),
    path('subscription_list/', views.subscription_list, name='subscription_list'),
    path('company_create/', views.company_create, name='company_create'),
    path('payment_create/', views.payment_create, name='payment_create'),
    path('payment_list/', views.payment_list, name='payment_list'),

    path("subscription/<int:pk>/update/", views.subscription_update, name="subscription_update"),
    path("payment/<int:pk>/update/", views.payment_update, name="payment_update"),
]