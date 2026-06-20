from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from . models import Product
from .forms import ProductForm, MarqueForm



# lister les produits
@login_required(login_url='accounts:login')
def product_list(request):
    products = Product.objects.filter(is_deleted=False).order_by('-created_at')
    context = {'products' : products}
    return render(request, "products/product_list.html", context)



# creation d'un produit
@login_required(login_url='accounts:login')
def create_product(request):

    if request.user.role not in ['owner']:
        return HttpResponseForbidden(
            "Vous n'avez pas la permission d'ajouter un produit."
        )

    if request.method == 'POST':

        form = ProductForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            return redirect(
                'products:product_list'
            )

    else:

        form = ProductForm()

    return render(
        request,
        'products/product_form.html',
        {
            'form': form
        }
    )



# creation d'un marque
@login_required(login_url='accounts:login')
def create_marque(request):

    if request.user.role not in ['owner']:
        return HttpResponseForbidden(
            "Vous n'avez pas la permission d'ajouter une marque."
        )

    if request.method == 'POST':

        form = MarqueForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(
                'products:create'
            )

    else:

        form = MarqueForm()

    return render(
        request,
        'products/marque_form.html',
        {
            'form': form
        }
    )




# mise à jour d'un produit
@login_required(login_url='accounts:login')
def update_product(request, pk):

    if request.user.role not in ['owner']:
        return HttpResponseForbidden(
            "Vous n'avez pas la permission à mettre à jour un Produit."
        )

    product = get_object_or_404(
        Product,
        id=pk
    )

    if request.method == 'POST':

        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():

            form.save()

            return redirect(
                'products:product_list'
            )

    else:

        form = ProductForm(
            instance=product
        )

    return render(
        request,
        'products/product_form.html',
        {
            'form': form
        }
    )



@login_required(login_url='accounts:login')
def delete_product(request, pk):
    if request.user.role not in ['owner']:
        return HttpResponseForbidden("Vous n'avez pas la permission de supprimer un Magasin.")
    product = get_object_or_404(Product, id=pk)
    product.is_deleted = True
    product.save()
    return redirect('products:product_list')