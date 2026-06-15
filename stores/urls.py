from django.urls import path
from . import views


app_name = "stores"

urlpatterns = [
    path('', views.store_list, name="store_list"),
    path('create/', views.create_store, name="create"),
    path('<int:pk>/update/', views.update_store, name="update"),
    path('<int:pk>/delete/', views.delete_store, name="delete"),

    path('<int:pk>/stock/', views.store_stock, name='store_stock'),
]