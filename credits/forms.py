from django import forms

from customers.models import Customer
from stores.models import Store
from .models import Credit, CreditPayment

class CreditForm(forms.ModelForm):

    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)

        if company:
            self.fields["customer"].queryset = (
                Customer.objects
                .for_company(company)
                .filter(is_deleted=False)
                .order_by("name")
            )

            self.fields["store"].queryset = (
                Store.objects
                .for_company(company)
                .filter(is_deleted=False)
                .order_by("name")
            )
            if not self.instance.pk and company:
                first_store = (
                    Store.objects
                    .for_company(company)
                    .filter(is_deleted=False)
                    .order_by("id")
                    .first()
                )
                if first_store:
                    self.fields["store"].initial = first_store

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

    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)

        if company:
            self.fields["credit"].queryset = (
                Credit.objects
                .for_company(company)
                .filter(is_deleted=False)
                .order_by("-id")
            )

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