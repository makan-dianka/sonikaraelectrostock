from django import forms

from accounts.models import CustomUser

from .models import (
    Company,
    Subscription,
    SubscriptionPlan,
    Payment
)

from django.db.models import Q


class CompanyForm(forms.ModelForm):

    # Champs de l'adresse
    street = forms.CharField(
        label="Rue / Adresse",
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ex : Hamdallaye ACI 2000"
        })
    )

    city = forms.CharField(
        label="Ville",
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ex : Bamako"
        })
    )

    postal_code = forms.CharField(
        label="Code postal",
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ex : BP 1234"
        })
    )

    country = forms.CharField(
        label="Pays",
        required=True,
        initial="Mali",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ex : Mali"
        })
    )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        queryset = CustomUser.objects.filter(
            role="owner"
        )

        if self.instance.pk:
            queryset = queryset.filter(
                Q(company__isnull=True) |
                Q(pk=self.instance.owner_id)
            )
        else:
            queryset = queryset.filter(
                company__isnull=True
            )

        self.fields["owner"].queryset = queryset.order_by(
            "first_name",
            "last_name",
        )

        # Si l'entreprise possède déjà une adresse,
        # on préremplit les champs.
        if self.instance.pk and self.instance.address:

            address = self.instance.address

            self.fields["street"].initial = address.street
            self.fields["city"].initial = address.city
            self.fields["postal_code"].initial = address.postal_code
            self.fields["country"].initial = address.country

    class Meta:

        model = Company

        fields = [
            "name",
            "owner",
            "subdomain",
            "phone",
            "email",
            "website",

            # Informations fiscales
            "nif",

            # Informations bancaires
            "rib",
            "bank_account",
            "bank_name",

            "is_active",
            "logo",

            # Adresse
            "street",
            "city",
            "postal_code",
            "country",
        ]

        widgets = {

            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nom de l'entreprise"
            }),

            "owner": forms.Select(attrs={
                "class": "form-control"
            }),

            "subdomain": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "sous domain"
            }),

            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Téléphone"
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "adresse email"
            }),

            "website": forms.URLInput(attrs={
                "class": "form-control",
                "placeholder": "https://example.com"
            }),

            "nif": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex : 08335454854W"
            }),

            "rib": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex : 50"
            }),

            "bank_account": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex : N 61600002201"
            }),

            "bank_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex : BMS.SA"
            }),

            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),

            "logo": forms.FileInput(attrs={
                "class": "form-control"
            }),
        }

        labels = {

            "name": "Entreprise",
            "owner": "Propriétaire",
            "subdomain": "Sous domaine",
            "phone": "Téléphone",
            "email": "Email",
            "website": "Site web",

            "nif": "NIF",

            "rib": "RIB",
            "bank_account": "Compte bancaire",
            "bank_name": "Banque",

            "is_active": "Entreprise active",
            "logo": "Logo",

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