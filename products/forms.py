from django import forms
from .models import Product


class ProductForm(forms.ModelForm):

    class Meta:

        model = Product

        exclude = [
            'is_deleted'
        ]

        widgets = {

            'name': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Nom du produit'
                }
            ),

            'category': forms.Select(
                attrs={
                    'class':'form-control'
                }
            ),

            'marque': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Marque'
                }
            ),

            'reference': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Référence'
                }
            ),

            'purchase_price': forms.NumberInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Prix achat'
                }
            ),

            'sale_price': forms.NumberInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Prix vente'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class':'form-control',
                    'rows':4,
                    'placeholder':'Description'
                }
            ),

            'image': forms.FileInput(
                attrs={
                    'class':'form-control'
                }
            ),

        }