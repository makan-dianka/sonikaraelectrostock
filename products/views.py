from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from . models import Category, Product, Marque
from .forms import ProductForm, MarqueForm
from stocks.models import Stock

from django.db.models import Q
from .models import Product
from .serializers import CategorySearchSerializer, ProductSearchSerializer, CategoryCreateSerializer, MarqueSearchSerializer
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_category_api(request):

    serializer = CategoryCreateSerializer(
        data=request.data,
        context={
            "request": request
        }
    )

    if serializer.is_valid():
        category = serializer.save()

        return Response({
            "success": True,
            "id": category.id,
            "name": category.name,
            "slug": category.slug,
        })

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_search_api(request):
    query = request.GET.get('q', '').strip()

    if len(query) < 1:
        return Response({'results': []})

    products = (
        Product.objects
        .for_company(request.user.company)
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




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def marque_search_api(request):

    query = request.GET.get('q', '').strip()

    marques = (
        Marque.objects
        .for_company(request.user.company)
        .filter(
            name__icontains=query
        )
        .order_by('name')
    )

    serializer = MarqueSearchSerializer(
        marques,
        many=True
    )

    return Response({
        'results': serializer.data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category_search_api(request):

    query = request.GET.get('q', '').strip()

    categories = (
        Category.objects
        .for_company(request.user.company)
        .filter(
            name__icontains=query
        )
        .order_by('name')
    )

    serializer = CategorySearchSerializer(
        categories,
        many=True
    )

    return Response({
        'results': serializer.data
    })




@login_required(login_url='accounts:login')
def product_list(request):

    q = request.GET.get('q', '').strip()

    products = (
        Product.objects
        .for_company(request.user.company)
        .filter(is_deleted=False)
        .prefetch_related(
            'stocks',
            'stocks__store'
        )
    )

    if q:
        products = products.filter(
            Q(name__icontains=q) |
            Q(reference__icontains=q)
        )

    products = products.order_by('-created_at')

    paginator = Paginator(products, 10)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'page_obj': page_obj,
        'q': q,
    }

    return render(request, 'products/product_list.html', context)



# creation d'un produit
@login_required(login_url='accounts:login')
def create_product(request):
    if request.user.role not in ['owner']:
        return HttpResponseForbidden("Vous n'avez pas la permission d'ajouter de produit.")


    form = ProductForm(request.POST or None, request.FILES or None, company=request.user.company)

    if form.is_valid():
        store = form.cleaned_data.pop('store')
        quantity = form.cleaned_data.pop('initial_stock')

        product = form.save(commit=False)
        product.company = request.user.company
        product.save()

        if store and quantity is not None:
            Stock.objects.create(
                company=request.user.company,
                product=product,
                store=store,
                quantity=quantity
            )

        return redirect('products:product_list')

    return render(request, 'products/product_form.html', {'form':form})



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
            marque = form.save(commit=False)
            marque.company = request.user.company
            marque.save()
            return redirect(
                'products:create'
            )

    else:
        form = MarqueForm()

    return render(request, 'products/marque_form.html', {'form': form})




# mise à jour d'un produit
@login_required(login_url="accounts:login")
def update_product(request, pk):

    if request.user.role not in ["owner"]:
        return HttpResponseForbidden(
            "Vous n'avez pas la permission de mettre à jour un produit."
        )

    company = request.user.company

    product = get_object_or_404(
        Product.objects.for_company(company),
        id=pk
    )

    # --------------------------------------------------
    # GET : récupérer le stock existant
    # --------------------------------------------------

    stock = (
        Stock.objects
        .for_company(company)
        .filter(product=product)
        .select_related("store")
        .first()
    )

    initial = {}

    if stock:
        initial = {
            "store": stock.store,
            "initial_stock": stock.quantity,
        }

    form = ProductForm(
        request.POST or None,
        request.FILES or None,
        instance=product,
        initial=initial,
        company=company,
    )

    if form.is_valid():

        store = form.cleaned_data.get("store")
        quantity = form.cleaned_data.get("initial_stock")

        product = form.save()

        if store:

            existing_stock = (
                Stock.objects
                .for_company(request.user.company)
                .filter(
                    product=product,
                    store=store
                )
                .first()
            )

            if existing_stock:

                existing_stock.quantity = quantity
                existing_stock.save(
                    update_fields=["quantity", "updated_at"]
                )

            else:

                old_stock = (
                    Stock.objects
                    .for_company(request.user.company)
                    .filter(
                        product=product,
                        store__isnull=True
                    )
                    .first()
                )

                if old_stock:

                    old_stock.store = store
                    old_stock.quantity = quantity
                    old_stock.save(
                        update_fields=["store", "quantity", "updated_at"]
                    )

                else:

                    Stock.objects.create(
                        company=request.user.company,
                        product=product,
                        store=store,
                        quantity=quantity
                    )

        return redirect("products:product_list")

    return render(
        request,
        "products/product_form.html",
        {
            "form": form,
        }
    )



@login_required(login_url='accounts:login')
def delete_product(request, pk):
    if request.user.role not in ['owner']:
        return HttpResponseForbidden("Vous n'avez pas la permission de supprimer un produit.")
    product = get_object_or_404(Product, id=pk, company=request.user.company)
    product.is_deleted = True
    product.save()
    return redirect('products:product_list')