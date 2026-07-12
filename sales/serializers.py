from rest_framework import serializers
from .models import Sale
from django.utils.formats import date_format


class SaleSearchSerializer(serializers.ModelSerializer):

    store = serializers.CharField(source='store.name', read_only=True)
    customer = serializers.CharField(source='customer.name', read_only=True)
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        fields = ['id', 'created_at', 'reference', 'customer', 'store', 'total', 'remaining_amount', 'status']


    def get_created_at(self, obj):
        return date_format(obj.created_at, "j F Y")