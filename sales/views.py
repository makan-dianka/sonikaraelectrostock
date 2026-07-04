from django.shortcuts import render, redirect, get_object_or_404

from django.utils import timezone

from .models import Sale

from .forms import SaleForm, SaleItemFormSet
from sonikaraelectrostock import tools

from django.contrib import messages
from django.db.models import Sum
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden

from .services import validate_sale, cancel_sale
from documents.services import generate_pdf
from django.http import FileResponse
from documents.models import Document

from django.contrib.auth.decorators import login_required


@login_required(login_url='accounts:login')
def print_invoice(request, pk):

    sale = get_object_or_404(
        Sale,
        pk=pk
    )

    document = Document.objects.filter(
        sale=sale,
        document_type="invoice"
    ).first()

    if not document:
        document = Document.objects.create(
            document_type='invoice',
            reference=tools.generate_reference('VTE', Document),
            sale=sale,
            generated_by=request.user,
        )
        generate_pdf(document)

    return FileResponse(document.pdf.open("rb"), content_type="application/pdf")



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
            if not sale.reference:
                sale.reference = tools.generate_reference('VTE', Sale)
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
def update_sale(request, pk):
    if request.user.role not in ['owner']:
        return HttpResponseForbidden("Vous n'avez pas la permission de modifier une vente.")


    sale = get_object_or_404(Sale, pk=pk)

    if request.method == 'POST':

        form = SaleForm(request.POST, instance=sale)
        formset = SaleItemFormSet(request.POST, instance=sale, prefix='items')

        if form.is_valid() and formset.is_valid():
            sale = form.save(commit=False)
            sale.user = request.user
            sale.save()

            formset.instance = sale
            formset.save()

            sale.recalc_total()

            return redirect('sales:list')

    else:
        form = SaleForm(instance=sale)
        formset = SaleItemFormSet(instance=sale, prefix='items')

    return render(request, 'sales/form.html', {
        'form': form,
        'formset': formset,
        'sale': sale
    })






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

    if request.user.role not in ['owner']:
        return HttpResponseForbidden("Vous n'avez pas la permission d'annuler une vente.")

    sale = (Sale.objects.get(id=pk))

    try:

        cancel_sale(sale)

        messages.success(request,"Vente annulé.")

    except Exception as e:

        messages.error(request, str(e))

    return redirect('sales:list')