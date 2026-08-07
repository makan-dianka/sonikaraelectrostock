from django import forms

from .models import Expense
from stores.models import Store


class ExpenseForm(forms.ModelForm):
    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)

        if company:
            self.fields["store"].queryset = (
                Store.objects
                .for_company(company)
                .filter(is_deleted=False)
            )

        # Sélectionner automatiquement le premier magasin de l'entreprise
        if not self.instance.pk and company:
            first_store = (
                Store.objects
                .for_company(company)
                .filter(is_deleted=False)
                .order_by("id")
                .first()
            )

            if first_store:
                self.fields["store"].initial = first_store

    class Meta:
        model = Expense
        exclude = [
            "reference",
            "created_by",
            "is_deleted",
            "company"
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