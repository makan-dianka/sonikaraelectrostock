from django import forms
from .models import Credit, CreditPayment

class CreditForm(forms.ModelForm):

    class Meta:

        model = Credit

        exclude = [
            "reference",
            "user",
            "status",
            "is_deleted"
        ]



        widgets = {

            'customer': forms.Select(
                attrs={
                    'class':'form-control'
                }
            ),

            'store': forms.Select(
                attrs={
                    'class':'form-control',
                }
            ),

            'amount': forms.NumberInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Montant'
                }
            ),

            'interest_rate': forms.NumberInput(
                attrs={
                    'class':'form-control',
                }
            ),

            'note': forms.Textarea(
                attrs={
                    'class':'form-control',
                    'rows':4,
                    'placeholder':'ajouter un commentaire'
                }
            ),


            'due_date': forms.DateInput(
                attrs={
                    'class':'form-control',
                    'type':'date'
                }
            ),

        }


        labels = {
            'customer': 'Choisir un client',
            'store': 'Choisir un magasin',
            'amount': "Montant du crédit",
            'interest_rate': "Taux d'intérêt en %",
            'note': "Commentaire",
            'due_date': "Date d'échéance",
        }






class CreditPaymentForm(forms.ModelForm):

    class Meta:

        model = CreditPayment

        exclude = [
            "is_deleted"
        ]



        widgets = {

            'credit': forms.Select(
                attrs={
                    'class':'form-control'
                }
            ),

            'payment_method': forms.Select(
                attrs={
                    'class':'form-control',
                }
            ),

            'amount': forms.NumberInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Montant'
                }
            ),

            'note': forms.Textarea(
                attrs={
                    'class':'form-control',
                    'rows':4,
                    'placeholder':'ajouter un commentaire'
                }
            ),

        }


        labels = {
            'credit': 'Choisir un crédit',
            'store': 'Choisir une methode de paiement',
            'amount': "Montant à payer",
            'note': "Commentaire",
        }