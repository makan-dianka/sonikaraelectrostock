from django import forms
from django.forms import inlineformset_factory

from .models import (
    Purchase,
    PurchaseItem
)


class PurchaseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['purchase_date'].input_formats = ['%Y-%m-%d']

    class Meta:
        model = Purchase
        exclude = [
            'total',
            'created_by',
            'status',
            'reference',
            'payment_status'
        ]

        widgets = {

            'supplier': forms.Select(
                attrs={
                    'class':'form-control'
                }
            ),

            'store': forms.Select(
                attrs={
                    'class':'form-control'
                }
            ),

            'purchase_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'class':'form-control',
                    'type':'date'
                }
            ),

            'notes': forms.Textarea(
                attrs={
                    'class':'form-control',
                    'rows':3
                }
            )
        }


        labels = {
            'supplier': "Choisir un fournisseur",
            'store': "Choisir un magasin",
            'purchase_date': "Date d'achat",
            'notes': 'Note',
        }


class PurchaseItemForm(forms.ModelForm):

    class Meta:
        model = PurchaseItem
        exclude = ['purchase', 'total']

        widgets = {

            'product': forms.HiddenInput(),   # <-- le changement clé

            'quantity': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': "Quantité",
                }
            ),

            'unit_price': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': "Prix d'achat"
                }
            )

        }

        labels = {
            'product': 'Produit',
            'quantity': 'Quantité',
            'unit_price': "Prix d'achat",
        }


PurchaseItemFormSet = (

    inlineformset_factory(

        Purchase,

        PurchaseItem,

        form=PurchaseItemForm,

        extra=1,

        can_delete=True

    )

)