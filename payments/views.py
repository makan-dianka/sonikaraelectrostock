from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .forms import (
    PaymentForm
)

from .models import (
    Payment
)

from sales.models import (
    Sale
)

from .services import (
    update_payment_status
)

from django.utils import timezone



# Generation of reference number
def generate_reference():

    """Generation of reference number

    Returns:
        str: reference number
    """

    now = timezone.now()

    prefix = (
        f"PYT-"
        f"{now:%Y%m}"
    )

    count = Payment.objects.count() + 1

    return (

        f"{prefix}"

        f"-{count:04d}"
    )





@login_required(login_url='accounts:login')
def create_payment(request, sale_id):

    sale = get_object_or_404(Sale, id=sale_id)

    form = PaymentForm(request.POST or None)

    if form.is_valid():

        payment = form.save(commit=False)

        if payment.amount > sale.remaining_amount:
            messages.error(request, "Montant trop élevé")
        else:
            payment.sale = sale

            payment.created_by = request.user
            payment.reference = generate_reference()
            payment.save()

            update_payment_status(sale)

            messages.success(request, "Paiement enregistré")

            return redirect('sales:list')
    else:
        form = PaymentForm(sale=sale)
    return render(request, 'payments/form.html', {'sale':sale, 'form':form})




@login_required(login_url='accounts:login')
def payment_list(request):
    payments = Payment.objects.select_related('sale').all().order_by('-id')
    return render(request, 'payments/list.html', {'payments': payments})