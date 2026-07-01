from django.shortcuts import render, redirect

from django.utils import timezone

from .models import Sale

from .forms import SaleForm, SaleItemFormSet

from django.contrib import messages
from django.db.models import Sum
from django.core.paginator import Paginator

from .services import validate_sale, cancel_sale

from django.contrib.auth.decorators import login_required



# Generation of reference number
def generate_reference():

    """Generation of reference number

    Returns:
        str: reference number
    """

    now = timezone.now()

    prefix = (
        f"VTE-"
        f"{now:%Y%m}"
    )

    count = Sale.objects.count() + 1

    return (

        f"{prefix}"

        f"-{count:04d}"
    )






@login_required(login_url='accounts:login')
def sale_list(request):

    sales = Sale.objects.select_related('customer', 'store').order_by('-created_at')

    sales_validated = Sale.objects.filter(status='validated').select_related('customer', 'store')
    total_sale = sales.filter(status='validated').aggregate(total=Sum('total'))['total'] or 0
    sales_validated = Sale.objects.filter(status='validated').select_related('customer', 'store').order_by('-created_at')
    total_paid = sum(sale.paid_amount for sale in sales_validated)
    total_remaining = total_sale - total_paid

    paginator = Paginator(sales, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'sales': page_obj,
        'page_obj': page_obj,
        'total_sale' : total_sale,
        'total_paid' : total_paid,
        'total_remaining' : total_remaining
    }

    return render(request, 'sales/list.html', context)



@login_required(login_url='accounts:login')
def create_sale(request):

    if request.method == 'POST':

        form = SaleForm(request.POST)

        sale = Sale()

        formset = SaleItemFormSet(request.POST, instance=sale, prefix='items')

        if form.is_valid() and formset.is_valid():
            sale = form.save(commit=False)
            sale.reference = generate_reference()
            sale.user = request.user
            sale.save()

            formset.instance = sale

            items = formset.save(commit=False)

            total = 0

            for item in items:

                item.subtotal = item.quantity * item.unit_price
                total += item.subtotal
                item.save()


            sale.total = total
            sale.save()
            return redirect('sales:list')

    else:

        form = SaleForm()

        formset = (
            SaleItemFormSet(
                prefix='items'
                )
            )

    return render(request, 'sales/form.html', {'form':form, 'formset':formset})




@login_required(login_url='accounts:login')
def validate_sale_view(request, pk):

    sale = (Sale.objects.get(id=pk))

    try:

        validate_sale(sale)

        messages.success(request,"Vente validée.")

    except Exception as e:

        messages.error(request, str(e))

    return redirect('sales:list')




@login_required(login_url='accounts:login')
def cancel_sale_view(request, pk):

    sale = (Sale.objects.get(id=pk))

    try:

        cancel_sale(sale)

        messages.success(request,"Vente annulé.")

    except Exception as e:

        messages.error(request, str(e))

    return redirect('sales:list')