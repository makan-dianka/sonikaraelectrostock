from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden

from .forms import PaymentForm
from .models import Payment
from sales.models import Sale
from purchases.models import Purchase
from .services import update_payment_status

from sonikaraelectrostock.tools import generate_reference



@login_required(login_url='accounts:login')
def create_payment(request):

    payment_type = request.GET.get('type')
    object_id = request.GET.get('id')
    if payment_type == None or object_id == None:
        return HttpResponseForbidden("Vous n'êtes pas authorisé à effectuer cette action.")

    obj = None
    form = None

    # verification de parametre url
    # et mettre à jour obj
    if payment_type == "sale":
        obj = get_object_or_404(Sale, id=object_id)
        form = PaymentForm(request.POST or None, sale=obj)

    elif payment_type == "purchase":
        obj = get_object_or_404(Purchase, id=object_id)
        form = PaymentForm(request.POST or None, purchase=obj)

    else:
        messages.error(request, "Type de paiement invalide")
        return redirect("dashboard:dashboard")


    if form.is_valid():

        payment = form.save(commit=False)

        payment.created_by = request.user
        payment.reference = generate_reference('PYT', Payment)

        # création de paiement pour
        # une vente
        if payment_type == "sale":

            if payment.amount > obj.remaining_amount:
                messages.error(request, "Montant trop élevé")
                return render(request, "payments/form.html", {
                    "form": form,
                    "object": obj,
                    "type": payment_type
                })

            payment.sale = obj
            payment.save()

            update_payment_status(obj)


        # création de paiement pour
        # un achat
        elif payment_type == "purchase":

            if payment.amount > obj.remaining_amount:
                messages.error(request, "Montant trop élevé")
                return render(request, "payments/form.html", {
                    "form": form,
                    "object": obj,
                    "type": payment_type
                })

            payment.purchase = obj
            payment.save()

            update_payment_status(obj)

        messages.success(request, "Paiement enregistré")

        return redirect("payments:list")

    return render(request, "payments/form.html", {
        "form": form,
        "object": obj,
        "type": payment_type
    })





# @login_required(login_url='accounts:login')
# def create_payment(request, sale_id):

#     sale = get_object_or_404(Sale, id=sale_id)

#     form = PaymentForm(request.POST or None)

#     if form.is_valid():

#         payment = form.save(commit=False)

#         if payment.amount > sale.remaining_amount:
#             messages.error(request, "Montant trop élevé")
#         else:
#             payment.sale = sale

#             payment.created_by = request.user
#             payment.reference = generate_reference()
#             payment.save()

#             update_payment_status(sale)

#             messages.success(request, "Paiement enregistré")

#             return redirect('sales:list')
#     else:
#         form = PaymentForm(sale=sale)
#     return render(request, 'payments/form.html', {'sale':sale, 'form':form})




@login_required(login_url='accounts:login')
def payment_list(request):
    payments = Payment.objects.select_related('sale').all().order_by('-id')
    return render(request, 'payments/list.html', {'payments': payments})