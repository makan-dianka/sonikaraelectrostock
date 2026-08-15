from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Company, Subscription, SubscriptionPlan, Payment, Address
from .forms import CompanyForm, SubscriptionForm, SubscriptionPlanForm, PaymentForm
from django.db.models import Sum
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from sonikaraelectrostock.tools import generate_reference
from datetime import date
from dateutil.relativedelta import relativedelta


@login_required(login_url='accounts:login')
def expired(request):
    return render(request, 'subscriptions/expired.html')

@login_required(login_url='accounts:login')
def subscription_plan(request):
    return render(request, 'subscriptions/subscription_plan.html')

@login_required(login_url='accounts:login')
def subscription_payment_info(request):
    return render(request, 'subscriptions/subscription_payment_info.html')



@login_required(login_url="accounts:login")
def dashboard(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    today = timezone.now().date()

    company_count = Company.objects.count()

    active_subscription = Subscription.objects.filter(status="active").count()
    expired_subscription = Subscription.objects.filter(end_date__lt=today).count()

    payment_year = (
        Payment.objects.filter(
            payment_date__year=today.year,
        ).aggregate(total=Sum("amount"))["total"] or 0
    )

    expiring_subscriptions = (
        Subscription.objects.filter(
            end_date__gte=today,
            end_date__lte=today + timedelta(days=15)
        )
        .select_related("company")
        .order_by("end_date")
    )

    last_payments = (
        Payment.objects
        .select_related("subscription__company")
        .order_by("-payment_date")[:10]
    )

    return render(request, "subscriptions/dashboard.html", {
        "company_count": company_count,
        "active_subscription": active_subscription,
        "expired_subscription": expired_subscription,
        "payment_year": payment_year,
        "expiring_subscriptions": expiring_subscriptions,
        "last_payments": last_payments,
    })



@login_required(login_url="accounts:login")
def company_create(request):

    if not request.user.is_superuser:
        return HttpResponseForbidden()

    form = CompanyForm(
        request.POST or None,
        request.FILES or None
    )

    if form.is_valid():

        with transaction.atomic():

            owner = form.cleaned_data["owner"]

            # Création de l'entreprise
            company = form.save(commit=False)
            company.owner = owner
            company.reference = generate_reference("CMP", Company)
            company.save()

            # Création de l'adresse
            address = Address.objects.create(
                street=form.cleaned_data["street"],
                city=form.cleaned_data["city"],
                postal_code=form.cleaned_data["postal_code"],
                country=form.cleaned_data["country"],
            )

            company.address = address
            company.save(update_fields=["address"])

            # Association du propriétaire
            owner.company = company
            owner.save(update_fields=["company"])

        messages.success(request, "Entreprise créée avec succès.")

        return redirect("subscriptions:dashboard")

    return render(
        request,
        "subscriptions/company_form.html",
        {
            "form": form,
            "title": "Nouvelle entreprise"
        }
    )



@login_required(login_url="accounts:login")
def company_list(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    companies = Company.objects.order_by("name")

    return render(request, "subscriptions/company_list.html", {"companies": companies})



@login_required(login_url="accounts:login")
def subscription_plan_list(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    subscriptions_plan = SubscriptionPlan.objects.order_by("name")

    return render(request, "subscriptions/subscription_plan_list.html", {"subscriptions_plan": subscriptions_plan})



@login_required(login_url="accounts:login")
def subscription_create(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    form = SubscriptionForm(request.POST or None)

    if form.is_valid():
        subscription = form.save(commit=False)
        subscription.reference = generate_reference('ABONN', Subscription)
        subscription.save()

        messages.success(request, "Abonnement créé.")

        return redirect("subscriptions:dashboard")

    return render(request, "subscriptions/subscription_form.html", {"form": form, "title": "Nouvel abonnement"})



@login_required(login_url="accounts:login")
def subscription_list(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Accès refusé.")

    subscriptions = (
        Subscription.objects
        .select_related("company", "plan")
        .order_by("-end_date")
    )

    return render(
        request,
        "subscriptions/subscription_list.html",
        {"subscriptions": subscriptions}
    )


@login_required(login_url="accounts:login")
def payment_list(request):

    if not request.user.is_superuser:
        return HttpResponseForbidden("Accès refusé.")

    payments = (
        Payment.objects
        .select_related("subscription__company")
        .order_by("-payment_date")
    )

    total = payments.aggregate(
        total=Sum("amount")
    )["total"] or 0

    return render(
        request,
        "subscriptions/payment_list.html",
        {
            "payments": payments,
            "total": total,
        }
    )



@login_required(login_url="accounts:login")
def payment_create(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Accès refusé.")

    form = PaymentForm(request.POST or None)

    if form.is_valid():

        payment = form.save(commit=False)
        payment.reference = generate_reference("PYT", Payment)
        payment.save()

        subscription = payment.subscription
        today = timezone.localdate()

        # Nombre de jours restant
        remaining_days = (subscription.end_date - today).days

        # --------------------------------------------------
        # ABONNEMENT EXPIRÉ OU ARRIVE À ÉCHÉANCE
        # --------------------------------------------------
        if remaining_days <= 2:

            if subscription.end_date >= today:
                # L'abonnement est encore valide,
                # mais il reste 2 jours ou moins.
                subscription.end_date = (
                    subscription.end_date + relativedelta(months=payment.period_month)
                )

            else:
                # L'abonnement est déjà expiré.
                subscription.start_date = today
                subscription.end_date = (today + relativedelta(months=payment.period_month))

            subscription.status = "active"
            subscription.trial = False
            subscription.save()

        # --------------------------------------------------
        # ABONNEMENT ENCORE LARGEMENT VALIDE
        # --------------------------------------------------
        # On enregistre uniquement le paiement.
        # Aucune modification de l'abonnement.

        return redirect("subscriptions:dashboard")

    return render(request, "subscriptions/payment_form.html", {"form": form})



@login_required(login_url="accounts:login")
def subscription_update(request, pk):

    if not request.user.is_superuser:
        return HttpResponseForbidden("Accès refusé.")

    subscription = get_object_or_404(
        Subscription.objects.select_related(
            "company",
            "plan"
        ),
        pk=pk
    )

    form = SubscriptionForm(
        request.POST or None,
        instance=subscription
    )

    if form.is_valid():

        form.save()

        return redirect(
            "subscriptions:subscription_list"
        )

    return render(
        request,
        "subscriptions/subscription_form.html",
        {
            "form": form,
            "subscription": subscription,
            "is_update": True,
        }
    )





@login_required(login_url="accounts:login")
def payment_update(request, pk):

    if not request.user.is_superuser:
        return HttpResponseForbidden("Accès refusé.")

    payment = get_object_or_404(
        Payment.objects.select_related(
            "subscription__company"
        ),
        pk=pk
    )

    form = PaymentForm(
        request.POST or None,
        instance=payment
    )

    if form.is_valid():

        form.save()

        return redirect(
            "subscriptions:payment_list"
        )

    return render(
        request,
        "subscriptions/payment_form.html",
        {
            "form": form,
            "payment": payment,
            "is_update": True,
        }
    )