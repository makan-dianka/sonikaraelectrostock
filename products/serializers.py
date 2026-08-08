# products/serializers.py
from rest_framework import serializers
from .models import Marque, Product, Category
from django.utils.text import slugify


class MarqueSearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Marque
        fields = ['id', 'name']


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



class CategoryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            "name",
            "description",
        ]

    def validate_name(self, value):

        company = self.context["request"].user.company

        exists = Category.objects.filter(
            company=company,
            name__iexact=value
        ).exists()

        if exists:
            raise serializers.ValidationError(
                "Cette catégorie existe déjà."
            )

        return value


    def create(self, validated_data):

        company = self.context["request"].user.company

        name = validated_data["name"]

        validated_data["company"] = company
        validated_data["slug"] = slugify(name)

        return super().create(validated_data)