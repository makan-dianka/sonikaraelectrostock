from rest_framework import serializers
from .models import Credit
from django.utils.formats import date_format


class CreditSearchSerializer(serializers.ModelSerializer):

    store = serializers.CharField(source='store.name', read_only=True)
    customer = serializers.CharField(source='customer.name', read_only=True)
    due_date = serializers.SerializerMethodField()

    class Meta:
        model = Credit
        fields = ['id', 'reference', 'customer', 'store', 'amount', 'remaining', 'interest_rate', 'note', 'due_date', 'status']


    def get_due_date(self, obj):
        return date_format(obj.due_date, "j F Y")