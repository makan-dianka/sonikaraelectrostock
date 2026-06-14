from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import Store
from .forms import StoreForm


# Liste de magasins
@login_required(login_url='accounts:login')
def store_list(request):
    stores = Store.objects.filter(deleted=False).order_by('-created_at')
    return render(request, 'stores/store_list.html', {'stores': stores})



# creation d'un magasin
@login_required(login_url='accounts:login')
def create_store(request):
    if request.user.role not in ['owner']:
        return HttpResponseForbidden("Vous n'avez pas la permission à créer un Magasin.")
    
    form = StoreForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('stores:store_list')
    return render(request, 'stores/store_form.html', {'form':form})



# mise à jour d'un magasin
@login_required(login_url='accounts:login')
def update_store(request, pk):
    if request.user.role not in ['owner']:
        return HttpResponseForbidden("Vous n'avez pas la permission à mettre à jour un Magasin.")
    
    store = get_object_or_404(Store, id=pk)
    form = StoreForm(request.POST or None, instance=store)
    if form.is_valid():
        form.save()
        return redirect('stores:store_list')
    return render(request, 'stores/store_form.html', {'form':form})


@login_required(login_url='accounts:login')
def delete_store(request, pk):
    if request.user.role not in ['owner']:
        return HttpResponseForbidden("Vous n'avez pas la permission de supprimer un Magasin.")
    store = get_object_or_404(Store, id=pk)
    store.deleted = True
    store.save()
    return redirect('stores:store_list')