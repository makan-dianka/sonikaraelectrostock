from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden

from accounts.forms import CreateUserForm
from .models import CustomUser




#######################################################################
# Création d'un collaborateur                -------------------------#
#######################################################################
@login_required(login_url='accounts:login')
def user_list(request):

    if request.user.is_owner():
        users = request.user.get_collaborators().select_related('store').order_by('first_name')
    else:
        users = CustomUser.objects.none()

    context = {
        'users': users,
        'total_users': users.count(),
        'total_manager': users.filter(role='manager').count(),
        'total_cashier': users.filter(role='cashier').count(),
        'total_seller': users.filter(role='seller').count(),
    }

    return render(request, 'accounts/user_list.html', context)




#######################################################################
# connexion de l'utilisateur à la plateforme -------------------------#
#######################################################################
def login_page(request):

    # si l'utilisateur est déjà authentifié
    # rediriger vers le tableau de bord
    if request.user.is_authenticated:
        return redirect("dashboard:dashboard")



    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard:dashboard') # -> redirection vers le tableau de bord
        else:
            messages.info(request, 'Votre email ou mot de passe est incorrect')
    return render(request, 'accounts/login.html')






#######################################################################
# inscription de l'utilisateur à la plateforme -----------------------#
#######################################################################

@login_required(login_url='accounts:login')
def register_page(request):
    # verifier si l'utilisateur a les droits d'accéder à cette page
    if request.user.role not in ['owner']:
        return HttpResponseForbidden("Vous n'avez pas la permission de créer un compte utilisateur.")


    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():

            form = form.save(commit=False)
            form.created_by = request.user
            form.save()

            return redirect('accounts:user_list')

        else:
            messages.info(request, 'Il y a une erreur dans le formulaire. Merci de corriger ')
    else:
        form = CreateUserForm()
    return render(request, 'accounts/register.html', {'form': form})



########################################################################
# deconnexion de l'utilisateur ----------------------------------------#
########################################################################
def logout_user(request):
    logout(request)
    return redirect('accounts:login')