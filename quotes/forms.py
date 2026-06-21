from django import forms
from django.forms import inlineformset_factory

from .models import Quote, QuoteItem


class QuoteForm(forms.ModelForm):

    class Meta:

        model = Quote

        exclude = [
            'reference',
            'user',
            'total',
            'is_deleted',
            'status',
            'pdf'
        ]

        widgets = {

            'customer':
            forms.Select(
                attrs={
                    'class':'form-control'
                }
            ),

            'store':
            forms.Select(
                attrs={
                    'class':'form-control'
                }
            ),

            'labor_cost':
            forms.NumberInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ex : 25 000'
                }
            ),

            'vat_rate':
            forms.NumberInput(
                attrs={
                    'class':'form-control',
                }
            ),

            'notes':
            forms.Textarea(
                attrs={
                    'class':'form-control'
                }
            ),

        }


        labels = {
            'customer': 'Choisir un client',
            'store': 'Choisir un magasin',
            'labor_cost': "Main d'oeuvre",
            'vat_rate': "Pourcentage TVA",
        }



class QuoteItemForm(forms.ModelForm):

    class Meta:

        model = QuoteItem

        exclude = ['quote', 'subtotal']

        widgets = {

            'product':
            forms.Select(
                attrs={
                    'class':'form-control'
                }
            ),

            'quantity':
            forms.NumberInput(
                attrs={
                    'class':'form-control'
                }
            ),

            'unit_price':
            forms.NumberInput(
                attrs={
                    'class':'form-control'
                }
            ),

        }


QuoteItemFormSet = inlineformset_factory(

    Quote,

    QuoteItem,

    form=QuoteItemForm,

    extra=1,

    can_delete=True

)