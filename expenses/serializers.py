from rest_framework import serializers
from .models import ExpenseCategory, Expense
from django.utils.formats import date_format

class ExpenseCategoryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExpenseCategory
        fields = ['name',]


    def validate_name(self, value):
        exists = ExpenseCategory.objects.filter(name=value).exists()
        if exists:
            raise serializers.ValidationError("Cette catégorie existe déjà.")
        return value
    

class ExpenseSearchSerializer(serializers.ModelSerializer):

    store = serializers.CharField(source='store.name', read_only=True)
    category = serializers.CharField(source='category.name', read_only=True)
    expense_date = serializers.SerializerMethodField()

    class Meta:
        model = Expense
        fields = ['id', 'reference', 'store', 'category', 'amount', 'description', 'expense_date', 'payment_method', 'created_by']


    def get_expense_date(self, obj):
        return date_format(obj.expense_date, "j F Y")