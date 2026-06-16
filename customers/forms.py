from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        exclude = [
            'is_deleted'
        ]

        widgets = {

            'name': forms.TextInput(
                attrs={
                    'class':'form-control'
                }
            ),

            'phone': forms.TextInput(
                attrs={
                    'class':'form-control'
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'class':'form-control'
                }
            ),

            'address': forms.Textarea(
                attrs={
                    'class':'form-control'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class':'form-control'
                }
            )
        }



        labels = {
            'name': 'Nom du client',
            'phone': 'Numéro de téléphone',
            'email': "Adresse email",
            'address': "Adresse domicile",
            'description': "Ajouter une note",
        }