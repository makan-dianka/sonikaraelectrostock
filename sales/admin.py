from django.contrib import admin
from .models import Sale


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('status', 'store', 'total', 'payment_status', 'user', 'created_at')