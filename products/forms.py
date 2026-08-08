from django import forms
from .models import Category, Product, Marque
from stores.models import Store


class ProductForm(forms.ModelForm):

    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["store"].queryset = (
            Store.objects
            .for_company(company)
            .filter(is_deleted=False)
        )

        self.fields["category"].queryset = (
            Category.objects
            .for_company(company)
        )

        self.fields["marque"].queryset = (
            Marque.objects
            .for_company(company)
        )

    store = forms.ModelChoiceField(
        queryset=Store.objects.none(),
        required=True,
        label="Magasin",
        widget=forms.Select(
            attrs={
                "class": "form-control"
            }
        )
    )


    initial_stock = forms.IntegerField(

        required=False,

        initial=0,

        label="Stock initial",

        widget=forms.NumberInput(

            attrs={

                'class':'form-control',

                'min':0

            }

        )

    )


    class Meta:

        model = Product

        fields = [

            'name',

            'category',

            'marque',

            'reference',

            'purchase_price',

            'sale_price',

            'description',

            'image',

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

            'marque': forms.HiddenInput(),

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

            'purchase_price': forms.NumberInput(
                attrs={
                    'class':'form-control',
                    'placeholder': "Prix d'achat"
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
            'purchase_price': "Prix d'achat",
            'image': "Image du produit",
        }




class MarqueForm(forms.ModelForm):

    class Meta:

        model = Marque


        fields = [

            'name',
            'note'

        ]

        widgets = {

            'name': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Nom du marque'
                }
            ),

            'note': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ajouter un commentaire (optionnel)'
                }
            ),

        }


        labels = {
            'name': 'Marque',
        }