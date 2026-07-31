from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden

from accounts.forms import CreateUserForm, UpdateUserForm
from .models import CustomUser
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import EmailMultiAlternatives
from django.db.models.query_utils import Q

from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.conf import settings
import os




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
            if user.is_active == False:
                messages.info(request, 'Votre compte est desactivé. Veuillez contacter votre employeur.')
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
        form = CreateUserForm(request.POST, current_user=request.user)
        if form.is_valid():

            form = form.save(commit=False)
            form.created_by = request.user
            form.company = request.user.company
            form.save()

            return redirect('accounts:user_list')

        else:
            messages.info(request, 'Il y a une erreur dans le formulaire. Merci de corriger ')
    else:
        form = CreateUserForm(current_user=request.user)
    return render(request, 'accounts/register.html', {'form': form})



########################################################################
# deconnexion de l'utilisateur ----------------------------------------#
########################################################################
def logout_user(request):
    logout(request)
    return redirect('accounts:login')



@login_required(login_url='accounts:login')
def user_settings(request):
    return render(request, 'accounts/settings.html')





@login_required(login_url='account:login')
def resetpwd(request):
    email = request.user.email
    if request.method=="POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.filter(Q(email=email))
            if user.exists():
                for user in user:
 
                    info = {
                        'username' : user.first_name,
                        'email': email,
                        'domain': os.getenv('DOMAIN'),
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'https://'
                    }

                    template_email = render_to_string('accounts/passwords/password_reset_email.html', info)
                    text_content = render_to_string('accounts/passwords/password_reset_email.txt', info)

                    objet = 'Réinitialisation du mot de passe'

                    email = EmailMultiAlternatives(
                        objet, 
                        text_content,
                        settings.EMAIL_HOST_USER, 
                        [email],
                        [settings.EMAIL_CC],
                        )

                    email.attach_alternative(template_email, "text/html")
                    email.fail_silently = False

  
                    try:
                        email.send()
                        return render(request, 'accounts/passwords/password_reset_done.html')
                    except Exception as e:
                        print(e)
                        print("Fail to send mail")
            else:
                messages.info(request, "[ Ce email n'exist pas ]")
                print("formulaire n'est pas valide.")
    form = PasswordResetForm()
    return render(request, 'accounts/passwords/resetpwd.html', {'form':form, 'email': email})





@login_required(login_url='account:login')
def edit_collaborator(request, user_id):
    user_obj = get_object_or_404(CustomUser, id=user_id)

    if request.user.role not in ['owner']:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à accéder à cette page.")

    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=user_obj, current_user=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:user_list')
    else:
        form = UpdateUserForm(instance=user_obj, current_user=request.user)

    return render(request, 'accounts/edit_collaborator.html', {'form': form})
