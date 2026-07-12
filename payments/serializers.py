from rest_framework import serializers
from .models import Payment
from django.utils.formats import date_format


class PaymentSearchSerializer(serializers.ModelSerializer):

    created_at = serializers.SerializerMethodField()
    sale = serializers.CharField(source='sale.reference', read_only=True)
    purchase = serializers.CharField(source='purchase.reference', read_only=True)
    sale_id = serializers.SerializerMethodField()
    purchase_id = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = ['id', 'sale', 'sale_id', 'purchase', 'purchase_id', 'amount', 'get_remaining', 'payment_method', 'reference', 'created_at']


    def get_created_at(self, obj):
        return date_format(obj.created_at, "j F Y")
    
    def get_sale_id(self, obj):
        return obj.sale.id if obj.sale else None

    def get_purchase_id(self, obj):
        return obj.purchase.id if obj.purchase else None