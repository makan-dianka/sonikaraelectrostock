from django.urls import path

from . import views

app_name='subscriptions'

urlpatterns=[
    path('expired/', views.expired, name='expired'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('subscription_plan/', views.subscription_plan, name='plan'),
    path('subscription_create/', views.subscription_create, name='subscription_create'),
    path('company_create/', views.company_create, name='company_create'),
    path('payment_create/', views.payment_create, name='payment_create'),
]