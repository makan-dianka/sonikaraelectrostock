# suppliers/serializers.py
from rest_framework import serializers
from .models import Supplier


class SupplierSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'phone', 'email', 'address']



class SupplierCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'phone', 'email', 'address']

    def validate_phone(self, value):
        exists = Supplier.objects.filter(phone=value, is_deleted=False).exists()
        if exists:
            raise serializers.ValidationError("Ce numéro existe déjà.")
        return value
