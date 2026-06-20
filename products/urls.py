from django.urls import path
from . import views


app_name = "products"

urlpatterns = [
    path('', views.product_list, name="product_list"),
    path('create/', views.create_product, name="create"),
    path('create/marque', views.create_marque, name="create_marque"),
    path('<int:pk>/update/', views.update_product, name="update"),
    path('<int:pk>/delete/', views.delete_product, name="delete"),


    # path('addstock/<int:product_id>/<int:store_id>/', views.add_stock, name='add_stock'),
]