from django.urls import path
from . import views


app_name = "accounts"

urlpatterns = [
    path('login/', views.login_page, name="login"),
    path('collaborators/', views.user_list, name="user_list"),
    path('register/', views.register_page, name="register"),
    path('logout/', views.logout_user, name="logout"),
]