from django import forms
from django.forms import inlineformset_factory

from .models import (
    Purchase,
    PurchaseItem
)


class PurchaseForm(forms.ModelForm):

    class Meta:
        model = Purchase
        exclude = [
            'total_amount',
            'created_by',
            'status',
            'invoice_number',
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


class PurchaseItemForm(forms.ModelForm):

    class Meta:
        model = PurchaseItem
        exclude = [
            'purchase',
            'total'
        ]

        widgets = {

            'product': forms.Select(
                attrs={
                    'class':'form-control',
                }
            ),

            'quantity': forms.NumberInput(
                attrs={
                    'class':'form-control',
                    'placeholder' : "Quantité"
                }
            ),

            'unit_price': forms.NumberInput(
                attrs={
                    'class':'form-control',
                    'placeholder' : "Prix d'achat"
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