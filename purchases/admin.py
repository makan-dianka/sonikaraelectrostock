from django.contrib import admin
from .models import Purchase, PurchaseItem


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'store', 'reference', 'total', 'status', 'created_by')



@admin.register(PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):
    list_display = ('purchase', 'product', 'quantity', 'unit_price', 'total')