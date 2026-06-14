from django.contrib import admin
from .models import Store

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone',)
    search_fields = ('name', 'address', 'phone')
    list_filter = ('name', 'phone',)