from django import forms
from .models import Store


class StoreForm(forms.ModelForm):

    class Meta:
        model = Store

        fields = [
            'name',
            'phone',
            'address',]

        widgets = {

            'name': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Nom du magasin'
                }
            ),

            'phone': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Téléphone'
                }
            ),

            'address': forms.Textarea(
                attrs={
                    'class':'form-control',
                    'placeholder':'Adresse',
                    'rows':3
                }
            ),

        }