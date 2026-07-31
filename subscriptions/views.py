from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Company, Subscription, SubscriptionPlan, Payment
from .forms import CompanyForm, SubscriptionForm, SubscriptionPlanForm, PaymentForm
from django.db.models import Sum
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



@login_required(login_url="accounts:login")
def dashboard(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    today = timezone.now().date()

    company_count = Company.objects.count()

    active_subscription = Subscription.objects.filter(status="active").count()
    expired_subscription = Subscription.objects.filter(end_date__lt=today).count()

    payment_month = (
        Payment.objects.filter(
            payment_date__month=today.month,
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
        "payment_month": payment_month,
        "expiring_subscriptions": expiring_subscriptions,
        "last_payments": last_payments,
    })



@login_required(login_url="accounts:login")
def company_create(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    form = CompanyForm(request.POST or None)

    if form.is_valid():
        form.reference = generate_reference('CMP', Company)
        form.save()
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
        return HttpResponseForbidden()

    subscriptions = Subscription.objects.order_by("name")

    return render(request, "subscriptions/subscription_list.html", {"subscriptions": subscriptions})


@login_required(login_url="accounts:login")
def payment_list(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    payments = Payment.objects.order_by("name")

    return render(request, "subscriptions/payment_list.html", {"payments": payments})




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

        today = date.today()

        # Si l'abonnement est encore actif
        if subscription.end_date >= today:
            subscription.end_date = subscription.end_date + relativedelta(months=payment.period_month)

        # Sinon on repart d'aujourd'hui
        else:
            subscription.start_date = today
            subscription.end_date = today + relativedelta(months=payment.period_month)

        subscription.status = "active"
        subscription.trial = False
        subscription.save()
        return redirect("subscriptions:dashboard")

    return render(request, "subscriptions/payment_form.html", {"form": form})