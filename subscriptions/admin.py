from django.contrib import admin
from .models import Company, SubscriptionPlan, Subscription, Payment

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'subdomain', 'phone', 'is_active', 'reference', "uuid", 'created_at')
    search_fields = ('name', 'phone', 'reference')
    list_filter = ('reference', 'is_active')


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'monthly_price', 'installation_fee', 'reference', 'active')
    search_fields = ('name', 'reference')
    list_filter = ('reference', 'active')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('company', 'plan', 'start_date', 'end_date', 'status', 'trial', 'reference', 'notes', 'updated_at')
    search_fields = ('company', 'plan')
    list_filter = ('reference', 'status')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('subscription', 'amount', 'payment_date', 'period_month', 'method', 'reference', 'notes', 'created_at')
    search_fields = ('reference', 'subscription')
    list_filter = ('reference', 'method')