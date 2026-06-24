from django import forms
from django.forms import inlineformset_factory

from .models import (
    Sale,
    SaleItem
)


class SaleForm(forms.ModelForm):

    class Meta:

        model = Sale

        exclude = [

            'reference',

            'user',

            'total',

            'status',

            'payment_status',

            'vat_rate'

        ]

        widgets = {

            'customer': forms.Select(
                attrs={
                    'class':'form-control'
                }
            ),

            'store': forms.Select(
                attrs={
                    'class':'form-control'
                }
            ),

            'apply_vat':forms.CheckboxInput(),

            'delivery_fee':forms.NumberInput(
                attrs={
                    'class':'form-control'
                }
            )

        }


        labels = {
            'customer': 'Choisir un client',
            'store': 'Choisir un magasin',
            'apply_vat': 'TVA',
            'delivery_fee': 'Frais de livraison',
        }




class SaleItemForm(forms.ModelForm):

    class Meta:
        model = SaleItem
        exclude = ['sale', 'subtotal']
        widgets = {
            'product': forms.HiddenInput(),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control'}),
        }


SaleItemFormSet = (

    inlineformset_factory(

        Sale,

        SaleItem,

        form=SaleItemForm,

        extra=1,

        can_delete=True

    )

)