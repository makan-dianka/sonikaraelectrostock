# products/serializers.py
from rest_framework import serializers
from .models import Product


# class ProductSearchSerializer(serializers.ModelSerializer):

#     category = serializers.CharField(source='category.name', read_only=True)

#     class Meta:
#         model = Product
#         fields = ['id', 'name', 'reference', 'category', 'purchase_price', 'sale_price']


class ProductSearchSerializer(serializers.ModelSerializer):

    category = serializers.CharField(source="category.name")

    marque = serializers.CharField(source="marque.name", default="")

    image = serializers.SerializerMethodField()

    stocks = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "reference",
            "category",
            "marque",
            "purchase_price",
            "sale_price",
            "image",
            "stocks",
        ]

    def get_image(self, obj):

        if obj.image:
            return obj.image.url

        return ""


    def get_stocks(self, obj):

        return [

            {
                "store":stock.store.name,
                "quantity":stock.quantity
            }

            for stock in obj.stocks.select_related("store")
        ]