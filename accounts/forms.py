from django import forms
from accounts.models import CustomUser
from stores.models import Store
from django.contrib.auth.forms import (
                                    UserCreationForm,
                                   )



class CreateUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user')
        super().__init__(*args, **kwargs)

        #--------- store queryset and initial value
        self.fields["store"].queryset = (
            Store.objects
            .for_company(current_user.company)
            .filter(is_deleted=False)
            .order_by("name")
        )
        if not self.instance.pk and current_user.company:
            first_store = (
                Store.objects
                .for_company(current_user.company)
                .filter(is_deleted=False)
                .order_by("id")
                .first()
            )
            if first_store:
                self.fields["store"].initial = first_store
        #--------- end of store queryset and initial value

        if current_user.role == 'platform_admin':
            self.fields['role'].choices = [
                ('owner', 'Propriétaire boutique'),
            ]

        elif current_user.role == 'owner':
            self.fields['role'].choices = [
                ('cashier', 'Caissier'),
                ('seller', 'Vendeur'),
                ('manager', 'Gérant'),
            ]
        else:
            self.fields['role'].choices = []

    password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Saisir un nouveau mot de passe'}), label="Mot de passe")
    password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmez votre mot de passe'}), label="Confirmer mot de passe")

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'role', 'store', 'email', 'phone', 'password1', 'password2']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Saisir votre prénom ici', 'required': 'required', 'type' : 'text'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Saisir votre nom ici', 'required': 'required', 'type' : 'text'}),
            'role': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'store': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Saisir votre adresse-email ici', 'type': 'email', 'required': 'required'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Saisir votre numéro de téléphone ici', 'required': 'required', 'type': 'text'}),
        }

        help_texts = {
            'username': None,
        }

        labels = {
            'first_name': 'Prénom',
            'last_name': 'Nom',
            'role': 'Rôle',
            'store': 'Magasin',
            'email': 'Adresse email',
            'phone': 'Numéro de téléphone',
        }




class UpdateUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user')
        super().__init__(*args, **kwargs)

        self.fields["store"].queryset = (
            Store.objects
            .for_company(current_user.company)
            .filter(is_deleted=False)
            .order_by("name")
        )

        if current_user.role == 'platform_admin':
            self.fields['role'].choices = [
                ('owner', 'Propriétaire boutique'),
            ]

        elif current_user.role == 'owner':
            self.fields['role'].choices = [
                ('cashier', 'Caissier'),
                ('seller', 'Vendeur'),
                ('manager', 'Gérant'),
            ]
        else:
            self.fields['role'].choices = []

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'role', 'store', 'email', 'phone', 'is_active']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'store': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(),
        }


        labels = {
            'first_name': 'Prénom',
            'last_name': 'Nom',
            'role': 'Rôle',
            'store': 'Magasin',
            'email': 'Adresse email',
            'phone': 'Numéro de téléphone',
            'is_active': 'Activer',
        }