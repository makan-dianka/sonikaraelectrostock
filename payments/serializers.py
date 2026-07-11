from rest_framework import serializers
from .models import Payment
from django.utils.formats import date_format


class PaymentSearchSerializer(serializers.ModelSerializer):

    created_at = serializers.SerializerMethodField()
    sale = serializers.CharField(source='sale.reference', read_only=True)
    purchase = serializers.CharField(source='purchase.reference', read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'sale', 'purchase', 'amount', 'get_remaining', 'payment_method', 'reference', 'created_at']


    def get_created_at(self, obj):
        return date_format(obj.created_at, "j F Y")