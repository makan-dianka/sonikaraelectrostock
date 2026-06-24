# products/serializers.py
from rest_framework import serializers
from .models import Product


class ProductSearchSerializer(serializers.ModelSerializer):

    category = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'reference', 'category', 'sale_price']