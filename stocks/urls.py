from django.urls import path
from . import views


app_name = "stocks"

urlpatterns = [
    path('addstock/<int:product_id>/<int:store_id>/', views.add_stock, name='add_stock'),
]