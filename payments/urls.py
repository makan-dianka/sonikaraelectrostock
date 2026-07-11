from django.urls import path
from common.search import search_api

from . import views

app_name='payments'

urlpatterns=[
    path('create/', views.create_payment, name='create'),
    path('', views.payment_list, name='list'),
    path("search/<str:entity>/", search_api, name="search_api"),
]