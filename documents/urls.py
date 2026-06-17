from django.urls import path

from . import views

app_name='documents'

urlpatterns=[
    path('', views.document_list, name='list'),
    path('create/', views.create_document, name='create'),
    path('delete/<int:pk>/', views.delete_document, name='delete'),
]