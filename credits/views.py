from django.shortcuts import render, redirect
from .forms import CreditForm
from .models import Credit, CreditPayment
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import CreditPaymentForm




# Generation of reference number
def generate_reference(obj, initial):

    """Generation of reference number

    Returns:
        str: reference number
    """

    now = timezone.now()

    prefix = (
        f"{initial.upper()}-"
        f"{now:%Y%m%d}"
    )

    count = obj.objects.count() + 1

    return (

        f"{prefix}"

        f"-{count:04d}"
    )





@login_required(login_url='accounts:login')
def create_credit(request):
    if request.user.role not in ['owner']:
        return HttpResponseForbidden(
            "Vous n'avez pas la permission de faire un crédit."
        )

    if request.method == "POST":
        form = CreditForm(request.POST)

        if form.is_valid():
            credit = form.save(commit=False)

            credit.user = request.user
            credit.reference = generate_reference(Credit, 'CR')

            credit.save()

            return redirect('credits:credit_list')

    else:
        form = CreditForm()

    return render(request, 'credits/form.html', {'form': form})




@login_required(login_url='accounts:login')
def credit_list(request):
    credits = Credit.objects.select_related('customer', 'store').all().order_by('-id')
    return render(request, 'credits/list.html', {'credits': credits})








@login_required(login_url='accounts:login')
def create_credit_payment(request):
    if request.user.role not in ['owner']:
        return HttpResponseForbidden(
            "Vous n'avez pas la permission de faire le paiement d'un crédit."
        )

    if request.method == "POST":

        form = CreditPaymentForm(request.POST)

        if form.is_valid():

            payment = form.save(commit=False)
            payment.reference = generate_reference(CreditPayment, 'CRPY')
            payment.save()

            return redirect("credits:credit_remboursement")

    else:

        form = CreditPaymentForm()

    return render(request, "credits/payment.html", {"form": form})




@login_required(login_url='accounts:login')
def credit_remboursement(request):

    payments = (

        CreditPayment.objects

        .select_related(
            'credit'
        )

        .filter(
            is_deleted=False
        )

        .order_by(
            '-id'
        )

    )

    return render(

        request,

        'credits/payment_list.html',

        {

            'payments': payments

        }

    )