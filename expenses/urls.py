from django.urls import path

from common.search import search_api

from . import views

app_name = "expenses"

urlpatterns = [
    path("", views.expense_list, name="list"),
    path("create/", views.expense_create, name="create"),
    path('<int:pk>/delete/', views.delete_expense, name="delete"),
    path('api/expense-category/create/', views.create_expense_category_api, name='create_expense_category_api'),

    path("search/<str:entity>/", search_api, name="search_api"),
]