from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from .models import Purchase

from .forms import (
    PurchaseForm,
    PurchaseItemFormSet
)

from django.contrib import messages
from django.db.models import Sum
from django.core.paginator import Paginator


from .services import receive_purchase


from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden



@login_required(login_url='accounts:login')
def purchase_list(request):

    purchases = (
        Purchase.objects
        .select_related(
            'supplier',
            'store'
        )
        .order_by(
            '-created_at'
        )
    )


    total_purchase = purchases.aggregate(total=Sum('total'))['total'] or 0
    total_paid = sum(purchase.paid_amount for purchase in purchases)
    total_remaining = total_purchase - total_paid


    paginator = Paginator(purchases, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'purchases': page_obj,
        'page_obj': page_obj,
        'total_purchase': total_purchase,
        'total_paid': total_paid,
        'total_remaining': total_remaining,
    }

    return render(request, 'purchases/list.html', context)





@login_required(login_url='accounts:login')
def purchase_create(request):
    if request.user.role not in ['owner']:
        return HttpResponseForbidden("Vous n'avez pas la permission d'effectuer un achat.")

    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            purchase = (
                form.save(commit=False)
            )

            purchase.created_by = (request.user)
            purchase.save()

            formset = (
                PurchaseItemFormSet(
                    request.POST,
                    instance=purchase,
                    prefix='items'
                )
            )

            if formset.is_valid():
                formset.save()
                return redirect('purchases:list')
    else:
        form = PurchaseForm()
        formset = (
            PurchaseItemFormSet(
                prefix='items'
            )
        )

    return render(request, 'purchases/form.html', {'form':form, 'formset':formset})






#################################################################
# Modifier l'état d'un achat :
# passer de Brouillon -> Receptionné ou annulé
#################################################################

@login_required(login_url='accounts:login')
def update_status(request, pk, status):

    if request.user.role not in ['owner']:
        return HttpResponseForbidden("Vous n'avez pas la permission de changer l'état de l'achat.")

    purchase = get_object_or_404(Purchase,id=pk)
    if not purchase.can_change_to(status):
        messages.error(request, "Transition impossible")
        return redirect('purchases:list')

    if status == 'received':
        receive_purchase(purchase)
        purchase.update_total() # mettre à jour le total dans l'entité purchase
    elif status == 'cancelled':
        purchase.status = 'cancelled'
        purchase.save()

    messages.success(request, "Statut mis à jour")
    return redirect('purchases:list')