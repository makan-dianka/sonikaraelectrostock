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
from common.pagination import paginate_queryset


from .services import receive_purchase, cancel_purchase


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


    total_purchase = purchases.filter(status='received').aggregate(total=Sum('total'))['total'] or 0
    total_paid = sum(purchase.paid_amount for purchase in purchases)
    total_remaining = total_purchase - total_paid


    page_obj = paginate_queryset(request, purchases)

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
            purchase = form.save(commit=False)
            purchase.created_by = request.user
            purchase.save()

            formset = PurchaseItemFormSet(
                request.POST,
                instance=purchase,
                prefix='items'
            )

            if formset.is_valid():
                formset.save()
                purchase.update_total() # mettre à jour le total dans l'entité purchase
                return redirect('purchases:list')
    else:
        form = PurchaseForm()
        formset = PurchaseItemFormSet(prefix='items')

    return render(request, 'purchases/form.html', {'form':form, 'formset':formset})




#################################################################
# Modifier un achat :
# fournisseur, produit ...
#################################################################
@login_required(login_url='accounts:login')
def update_purchase(request, pk):
    if request.user.role not in ['owner']:
        return HttpResponseForbidden("Vous n'avez pas la permission de modifier un achat.")


    purchase = get_object_or_404(Purchase, pk=pk)

    if request.method == 'POST':

        form = PurchaseForm(request.POST, instance=purchase)
        formset = PurchaseItemFormSet(request.POST, instance=purchase, prefix='items')

        if form.is_valid() and formset.is_valid():
            purchase = form.save(commit=False)
            purchase.user = request.user
            purchase.save()

            formset.instance = purchase
            formset.save()

            purchase.recalc_total()

            return redirect('purchases:list')

    else:
        form = PurchaseForm(instance=purchase)
        formset = PurchaseItemFormSet(instance=purchase, prefix='items')

    return render(request, 'purchases/form.html', {
        'form': form,
        'formset': formset,
        'purchase': purchase
    })






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
    elif status == 'cancelled':
        cancel_purchase(purchase)

    messages.success(request, "Statut mis à jour")
    return redirect('purchases:list')