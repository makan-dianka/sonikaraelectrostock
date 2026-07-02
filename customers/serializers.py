# products/serializers.py
from rest_framework import serializers
from .models import Customer


class CustomerSearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['id', 'name', 'phone', 'email', 'address']





class CustomerCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email', 'address', 'description',]


    def validate_phone(self, value):
        exists = Customer.objects.filter(phone=value, is_deleted=False).exists()
        if exists:
            raise serializers.ValidationError("Ce numéro existe déjà.")
        return value