from django.urls import path
from . import views


app_name = "dashboard"

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('store/<int:store_id>', views.dashboard, name="dashboard_store"),
    path('rapport/', views.rapport, name="rapport"),
    path('rapport/store/<int:store_id>', views.rapport, name="rapport_store"),
]