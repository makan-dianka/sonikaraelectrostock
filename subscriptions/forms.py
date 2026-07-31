from django import forms

from .models import (
    Company,
    Subscription,
    SubscriptionPlan,
    Payment
)


class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = [
            "name",
            "owner",
            "subdomain",
            "phone",
            "email",
            "is_active",
        ]

        widgets = {

            "name": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "owner": forms.Select(attrs={
                "class": "form-control"
            }),

            "subdomain": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "phone": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control"
            }),

            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),

        }

        labels = {

            "name": "Entreprise",

            "owner": "Propriétaire",

            "subdomain": "Sous domaine",

            "phone": "Téléphone",

            "email": "Email",

            "is_active": "Entreprise active",

        }






class SubscriptionForm(forms.ModelForm):

    class Meta:

        model = Subscription

        fields = [
            "company",
            "plan",
            "start_date",
            "end_date",
            "status",
            "trial",
            "notes",
        ]

        widgets = {

            "company": forms.Select(attrs={
                "class": "form-control"
            }),

            "plan": forms.Select(attrs={
                "class": "form-control"
            }),

            "start_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),

            "end_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),

            "status": forms.Select(attrs={
                "class": "form-control"
            }),

            "trial": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),

            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4
                }
            ),

        }

        labels = {

            "company": "Entreprise",

            "plan": "Abonnement",

            "start_date": "Début",

            "end_date": "Fin",

            "status": "Statut",

            "trial": "Période d'essai",

            "notes": "Notes",

        }




class PaymentForm(forms.ModelForm):

    class Meta:

        model = Payment

        fields = [
            "subscription",
            "amount",
            "payment_date",
            "period_month",
            "method",
            "notes",
        ]

        widgets = {

            "subscription": forms.Select(attrs={
                "class": "form-control"
            }),

            "amount": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "payment_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),

            "period_month": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "method": forms.Select(attrs={
                "class": "form-control"
            }),

            "notes": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4
            }),

        }

        labels = {

            "subscription": "Entreprise",

            "amount": "Montant",

            "payment_date": "Date de paiement",

            "period_month": "Nombre de mois",

            "method": "Méthode de paiement",

            "notes": "Notes",

        }




class SubscriptionPlanForm(forms.ModelForm):

    class Meta:

        model = SubscriptionPlan

        fields = [

            "name",
            "monthly_price",
            "installation_fee",
            "active",

        ]

        widgets = {

            "name": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "monthly_price": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "installation_fee": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "active": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),

        }

        labels = {

            "name": "Nom",

            "monthly_price": "Prix mensuel",

            "installation_fee": "Frais d'installation",

            "active": "Actif",

        }