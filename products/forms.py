from django import forms
from .models import Product


class ProductForm(forms.ModelForm):

    class Meta:

        model = Product

        exclude = [
            'is_deleted',
            'purchase_price',
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


        labels = {
            'name': 'Nom du produit',
            'category': 'Catégorie',
            'reference': "Référence",
            'sale_price': "Prix de vente",
            'image': "Image du produit",
        }