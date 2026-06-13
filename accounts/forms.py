from django import forms
from accounts.models import CustomUser
from django.contrib.auth.forms import (
                                    UserCreationForm,
                                   )



class CreateUserForm(UserCreationForm):

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