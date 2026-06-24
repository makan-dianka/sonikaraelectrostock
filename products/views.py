from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from . models import Product
from .forms import ProductForm, MarqueForm
from stocks.models import Stock

from django.db.models import Q
from .models import Product
from .serializers import ProductSearchSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_search_api(request):
    query = request.GET.get('q', '').strip()

    if len(query) < 1:
        return Response({'results': []})

    products = (
        Product.objects
        .filter(is_deleted=False)
        .filter(
            Q(reference__icontains=query) |
            Q(name__icontains=query) |
            Q(category__name__icontains=query)
        )
        .select_related('category')
        .order_by('name')[:20]
    )

    serializer = ProductSearchSerializer(products, many=True)
    return Response({'results': serializer.data})



# lister les produits
@login_required(login_url='accounts:login')
def product_list(request):
    products = Product.objects.filter(is_deleted=False).order_by('-created_at')
    context = {'products' : products}
    return render(request, "products/product_list.html", context)



# creation d'un produit
@login_required(login_url='accounts:login')
def create_product(request):

    form = ProductForm(

        request.POST or None,

        request.FILES or None

    )


    if form.is_valid():

        store = (

            form.cleaned_data.pop(
                'store'
            )
        )

        quantity = (

            form.cleaned_data.pop(
                'initial_stock'
            )
        )


        product = (

            form.save()
        )


        if (

            store

            and

            quantity

        ):

            Stock.objects.create(

                product=product,

                store=store,

                quantity=quantity

            )


        return redirect(

            'products:product_list'

        )


    return render(

        request,

        'products/product_form.html',

        {

            'form':form

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


    initial = {}

    stock = product.stocks.first()
    if stock:
        initial = {
            'store': stock.store,
            'initial_stock': stock.quantity
        }


    form = ProductForm(
        request.POST or None,
        request.FILES or None,
        instance=product,
        initial=initial
    )



    if request.method == 'POST':

        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():
            store = form.cleaned_data.pop('store')
            quantity = form.cleaned_data.pop('initial_stock')
            product = form.save()

            if store:
                Stock.objects.update_or_create(
                    product=product,
                    store=store,
                    defaults={
                        'quantity':quantity
                    }
                )

            return redirect('products:product_list')

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