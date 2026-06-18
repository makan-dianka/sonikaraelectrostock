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

        }


        labels = {
            'customer': 'Choisir un client',
            'store': 'Choisir un magasin',
        }




class SaleItemForm(forms.ModelForm):

    class Meta:

        model = SaleItem

        exclude = [

            'sale',

            'subtotal'

        ]

        widgets = {

            'product': forms.Select(
                attrs={
                    'class':'form-control'
                }
            ),

            'quantity': forms.NumberInput(
                attrs={
                    'class':'form-control'
                }
            ),

            'unit_price': forms.NumberInput(
                attrs={
                    'class':'form-control'
                }
            )

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