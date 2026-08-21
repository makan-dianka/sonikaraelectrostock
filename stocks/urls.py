from django.urls import path
from . import views
from common.search import search_api


app_name = "stocks"

urlpatterns = [
    # path('addstock/<int:product_id>/<int:store_id>/', views.add_stock, name='add_stock'),

    path('search/<str:entity>/', search_api, name='search_api'),
]