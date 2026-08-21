from rest_framework import serializers
from .models import Stock


class StockSearchSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_categ = serializers.CharField(source="product.category", read_only=True)
    product_reference = serializers.CharField(source="product.reference", read_only=True)

    class Meta:
        model = Stock
        fields = [
            "id",
            "product_name",
            "product_reference",
            "quantity",
            "alert_threshold",
            'product_categ'
        ]