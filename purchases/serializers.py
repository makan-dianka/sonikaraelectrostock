from rest_framework import serializers
from .models import Purchase
from django.utils.formats import date_format


class PurchaseSearchSerializer(serializers.ModelSerializer):

    store = serializers.CharField(source='store.name', read_only=True)
    supplier = serializers.CharField(source='supplier.name', read_only=True)
    purchase_date = serializers.SerializerMethodField()

    class Meta:
        model = Purchase
        fields = ['id', 'purchase_date', 'reference', 'supplier', 'store', 'total', 'remaining_amount', 'status', 'payment_status']


    def get_purchase_date(self, obj):
        return date_format(obj.created_at, "j F Y")