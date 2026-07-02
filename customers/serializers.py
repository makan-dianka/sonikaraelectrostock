# products/serializers.py
from rest_framework import serializers
from .models import Customer


class CustomerSearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['id', 'name', 'phone', 'email', 'address']