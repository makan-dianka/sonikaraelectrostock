from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import Customer
from .forms import CustomerForm




@login_required(login_url='accounts:login')
def customer_list(request):

    customers = (
        Customer.objects.filter(
            is_deleted=False
        )
    )
    return render(request, 'customers/list.html', {'customers': customers})



@login_required(login_url='accounts:login')
def customer_create(request):
    if request.user.role not in ['owner']:
        return HttpResponseForbidden("Vous n'avez pas la permission d'ajouter un client.")
    form = CustomerForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('customers:list')

    return render(request, 'customers/form.html', {'form':form})




# mise à jour d'un client
@login_required(login_url='accounts:login')
def update_customer(request, pk):
    if request.user.role not in ['owner']:
        return HttpResponseForbidden("Vous n'avez pas la permission à mettre à jour le client.")

    customer = get_object_or_404(Customer, id=pk)
    form = CustomerForm(request.POST or None, instance=customer)
    if form.is_valid():
        form.save()
        return redirect('customers:list')
    return render(request, 'customers/form.html', {'form':form})





@login_required(login_url='accounts:login')
def delete_customer(request, pk):
    if request.user.role not in ['owner']:
        return HttpResponseForbidden("Vous n'avez pas la permission de supprimer un client.")
    customer = get_object_or_404(Customer, id=pk)
    customer.is_deleted = True
    customer.save()
    return redirect('customers:list')