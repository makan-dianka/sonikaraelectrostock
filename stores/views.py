from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

from .models import Store
from .forms import StoreForm
from stocks.models import Stock
from common.pagination import paginate_queryset



# Liste de magasins
@login_required(login_url='accounts:login')
def store_list(request):
    stores = Store.objects.for_company(request.user.company).filter(is_deleted=False).order_by('-created_at')

    context = {
        'stores': stores,
        'has_store': stores.exists(),
    }
    return render(request, 'stores/store_list.html', context)



# creation d'un magasin
@login_required(login_url='accounts:login')
def create_store(request):
    if request.user.role not in ['owner']:
        return HttpResponseForbidden("Vous n'avez pas la permission à créer un Magasin.")

    company = request.user.company

    # Blocage si l'entreprise possède déjà un magasin actif (non supprimé)
    if company.stores.filter(is_deleted=False).exists():
        messages.error(request, "Votre entreprise possède déjà un magasin.")
        return redirect('stores:store_list')

    form = StoreForm(request.POST or None)
    if form.is_valid():
        store = form.save(commit=False)
        store.company = request.user.company
        store.save()
        return redirect('stores:store_list')
    return render(request, 'stores/store_form.html', {'form':form})



# mise à jour d'un magasin
@login_required(login_url='accounts:login')
def update_store(request, pk):
    if request.user.role not in ['owner']:
        return HttpResponseForbidden("Vous n'avez pas la permission à mettre à jour un Magasin.")
    
    store = get_object_or_404(Store.objects.for_company(request.user.company), id=pk)
    form = StoreForm(request.POST or None, instance=store)
    if form.is_valid():
        store = form.save(commit=False)
        store.company = request.user.company
        store.save()
        return redirect('stores:store_list')
    return render(request, 'stores/store_form.html', {'form':form})


@login_required(login_url='accounts:login')
def delete_store(request, pk):
    if request.user.role not in ['owner']:
        return HttpResponseForbidden("Vous n'avez pas la permission de supprimer un Magasin.")
    store = get_object_or_404(Store.objects.for_company(request.user.company), id=pk)

    has_stock = store.stocks.filter(quantity__gt=0).exists()
    has_sales = store.sales.exists()
    has_purchases = store.purchases.exists()

    if has_stock or has_sales or has_purchases:
        messages.error(request, "Impossible de supprimer ce magasin : il contient du stock ou possède un historique de ventes/achats.")
        return redirect('stores:store_list')


    store.is_deleted = True
    store.save()
    return redirect('stores:store_list')



@login_required(login_url='accounts:login')
def store_stock(request, pk):

    store = get_object_or_404(Store.objects.for_company(request.user.company), id=pk)
    stocks = (
        Stock.objects.for_company(request.user.company)
        .filter(store=store)
        .select_related('product', 'product__category')
        .order_by('product__name')
    )

    page_obj = paginate_queryset(request, stocks)

    context = {
        'store': store, 
        'stocks': page_obj, 
        'page_obj': page_obj,
        }
    return render(request, 'stores/store_stock.html', context)