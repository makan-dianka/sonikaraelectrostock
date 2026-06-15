from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import Supplier
from .forms import SupplierForm




@login_required(login_url='accounts:login')
def supplier_list(request):

    suppliers = (
        Supplier.objects.filter(
            is_deleted=False
        )
    )
    return render(request, 'suppliers/list.html', {'suppliers': suppliers})



@login_required(login_url='accounts:login')
def supplier_create(request):
    if request.user.role not in ['owner']:
        return HttpResponseForbidden("Vous n'avez pas la permission d'ajouter un fournisseur.")
    form = SupplierForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('suppliers:list')

    return render(request, 'suppliers/form.html', {'form':form})




# mise à jour d'un fournisseur
@login_required(login_url='accounts:login')
def update_supplier(request, pk):
    if request.user.role not in ['owner']:
        return HttpResponseForbidden("Vous n'avez pas la permission à mettre à jour le fournisseur.")

    supplier = get_object_or_404(Supplier, id=pk)
    form = SupplierForm(request.POST or None, instance=supplier)
    if form.is_valid():
        form.save()
        return redirect('suppliers:list')
    return render(request, 'suppliers/form.html', {'form':form})





@login_required(login_url='accounts:login')
def delete_supplier(request, pk):
    if request.user.role not in ['owner']:
        return HttpResponseForbidden("Vous n'avez pas la permission de supprimer un fournisseur.")
    supplier = get_object_or_404(Supplier, id=pk)
    supplier.is_deleted = True
    supplier.save()
    return redirect('suppliers:list')