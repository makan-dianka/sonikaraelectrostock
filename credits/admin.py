from django.contrib import admin
from .models import Credit, CreditPayment


@admin.register(Credit)
class CreditAdmin(admin.ModelAdmin):
    list_display = ('reference', 'customer', 'store', 'amount', 'due_date', 'status', 'created_at')



@admin.register(CreditPayment)
class CreditPaymentAdmin(admin.ModelAdmin):
    list_display = ('reference', 'credit', 'payment_method', 'amount', 'note', 'created_at')

