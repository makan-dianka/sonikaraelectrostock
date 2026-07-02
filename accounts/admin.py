from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'store', 'is_staff', 'is_active', "last_login")
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active')