from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Stock
from .forms import AddStockForm


# ajout de stock
@login_required(login_url='accounts:login')
def add_stock(request, product_id, store_id):
    if request.user.role not in ['owner']:
        return HttpResponseForbidden("Vous n'avez pas la permission d'ajouter du stock.")
    stock = get_object_or_404(Stock, product_id=product_id, store_id=store_id)
    form = AddStockForm(request.POST or None)
    if form.is_valid():
        stock.quantity += (form.cleaned_data['quantity'])
        stock.save()
        return redirect('stores:store_stock', store_id)
    return render(request, 'stocks/add_stock.html', {'form':form, 'stock':stock})
