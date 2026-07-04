from rest_framework import serializers
from .models import ExpenseCategory

class ExpenseCategoryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExpenseCategory
        fields = ['name',]


    def validate_name(self, value):
        exists = ExpenseCategory.objects.filter(name=value).exists()
        if exists:
            raise serializers.ValidationError("Cette catégorie existe déjà.")
        return value