
from django import forms
from django.forms import inlineformset_factory

from .models import (
    Sale,
    SaleItem
)
from stores.models import Store


class SaleForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Sélectionner automatiquement le premier magasin
        if not self.instance.pk:
            first_store = Store.objects.order_by('id').first()
            if first_store:
                self.fields['store'].initial = first_store



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

            'reduction':
            forms.NumberInput(
                attrs={
                    'class':'form-control',
                }
            ),

            'delivery_fee':forms.NumberInput(
                attrs={
                    'class':'form-control'
                }
            ),

            'warranty': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': "Écrire la garantie ici..."
                }
            ),

        }


        labels = {
            'customer': 'Choisir un client',
            'store': 'Choisir un magasin',
            'vat_rate': 'Pourcentage TVA (%)',
            'delivery_fee': 'Frais de livraison',
            'warranty': "Garantie",
            'reduction': "Réduction (%)",
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



    # empecher une vente si le prix de vente est inferieur
    # ou egal au prix d'achat
    def clean(self):
        cleaned_data = super().clean()

        product = cleaned_data.get('product')
        unit_price = cleaned_data.get('unit_price')

        if product and unit_price is not None:
            purchase_price = product.purchase_price

            if unit_price <= purchase_price:
                raise forms.ValidationError(
                    f"Le prix de vente ({unit_price} FCFA) doit être supérieur au prix d'achat ({purchase_price} FCFA)."
                )

        return cleaned_data



SaleItemFormSet = (

    inlineformset_factory(

        Sale,

        SaleItem,

        form=SaleItemForm,

        extra=1,

        can_delete=True

    )

)