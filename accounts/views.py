from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages




#######################################################################
# connexion de l'utilisateur à la plateforme -------------------------#
#######################################################################
def login_page(request):

    # si l'utilisateur est déjà authentifié
    # rediriger vers le tableau de bord
    if request.user.is_authenticated:
        return redirect("productapp:home")



    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:

            # empecher utilisateur de se connecter
            # si son adresse email n'est pas confirmer
            if not user.is_email_verified:
                messages.error(request, 'Veuillez confirmer votre email.')
                return redirect('accounts:login')


            # si email et mdp sont corrects
            # si email validé, alors 
            # connexion autorisé
            login(request, user)
            return redirect('productapp:home') # -> redirection vers le tableau de bord
        else:
            messages.info(request, 'Votre email ou mot de passe est incorrect')
    return render(request, 'accounts/login.html')