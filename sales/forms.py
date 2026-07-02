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

        ]

        widgets = {

            'customer': forms.HiddenInput(),

            'store': forms.Select(
                attrs={
                    'class':'form-control'
                }
            ),

            'vat_rate':
            forms.NumberInput(
                attrs={
                    'class':'form-control',
                }
            ),

            'delivery_fee':forms.NumberInput(
                attrs={
                    'class':'form-control'
                }
            )

        }


        labels = {
            'customer': 'Choisir un client',
            'store': 'Choisir un magasin',
            'vat_rate': 'Pourcentage TVA (%)',
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