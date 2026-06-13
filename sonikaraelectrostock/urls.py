from django.contrib import admin
from django.urls import path, include


app_name = "accounts"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("accounts.urls")),
    path('', include("dashboard.urls")),
]
