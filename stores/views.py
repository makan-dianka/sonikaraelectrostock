from django.shortcuts import render, redirect, get_object_or_404
from .models import Store
from .forms import StoreForm


# Liste de magasins
def store_list(request):
    stores = Store.objects.filter(deleted=False).order_by('-created_at')
    return render(request, 'stores/store_list.html', {'stores': stores})



# creation d'un magasin
def create_store(request):
    form = StoreForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('stores:store_list')
    return render(request, 'stores/store_form.html', {'form':form})



# mise à jour d'un magasin
def update_store(request, pk):
    store = get_object_or_404(Store, id=pk)
    form = StoreForm(request.POST or None, instance=store)
    if form.is_valid():
        form.save()
        return redirect('stores:store_list')
    return render(request, 'stores/store_form.html', {'form':form})



def delete_store(request, pk):
    store = get_object_or_404(Store, id=pk)
    store.deleted = True
    store.save()
    return redirect('stores:store_list')