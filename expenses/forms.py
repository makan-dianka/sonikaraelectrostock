from django import forms

from .models import Expense


class ExpenseForm(forms.ModelForm):

    class Meta:
        model = Expense
        exclude = [
            "reference",
            "created_by",
            "is_deleted",
        ]

        widgets = {

            "store": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "category": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Montant"
                }
            ),

            "expense_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),

            "payment_method": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4
                }
            )

        }

        labels = {

            "store": "Magasin",
            "category": "Catégorie",
            "amount": "Montant",
            "expense_date": "Date",
            "payment_method": "Mode de paiement",
            "description": "Description"
        }