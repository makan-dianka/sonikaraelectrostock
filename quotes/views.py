from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.http import FileResponse
from .models import Quote
from .forms import (
    QuoteForm,
    QuoteItemFormSet
)


from django.template.loader import render_to_string
from sonikaraelectrostock.tools import generate_reference

from django.core.files.base import ContentFile

from weasyprint import HTML

from django.conf import settings
import os
from django.utils import timezone
from django.core.paginator import Paginator




@login_required(login_url='accounts:login')
def print_quote(request, pk):

    quote = get_object_or_404(
        Quote,
        pk=pk
    )

    generate_quote_pdf(quote)

    return FileResponse(quote.pdf.open("rb"), content_type="application/pdf")






@login_required(login_url='accounts:login')
def quote_list(request):

    quotes = (

        Quote.objects

        .select_related(
            'customer',
            'store'
        )

        .order_by(
            '-created_at'
        )

    )



    paginator = Paginator(quotes, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'quotes': page_obj,
        'page_obj': page_obj,
    }

    return render(request, 'quotes/list.html', context)




@login_required(login_url='accounts:login')
def create_quote(request):
    if request.user.role not in ['owner']:
        return HttpResponseForbidden(
            "Vous n'avez pas la permission créer un devis."
        )

    form = QuoteForm(

        request.POST or None

    )

    formset = QuoteItemFormSet(

        request.POST or None,

        prefix='items'

    )


    if (

        form.is_valid()

        and

        formset.is_valid()

    ):

        print("data posted :", request.POST)
        print("form error : ", formset.errors)
        print("Non form", formset.non_form_errors())


        quote = (

            form.save(
                commit=False
            )
        )

        quote.reference = generate_reference('DEV', Quote)

        quote.user = (

            request.user
        )

        quote.save()

        items = formset.save(
            commit=False
        )

        total = 0

        for item in items:

            item.quote = quote

            item.subtotal = (
                item.quantity
                *
                item.unit_price
            )

            total += item.subtotal

            item.save()


        for deleted in formset.deleted_objects:
            deleted.delete()


        quote.total = total

        quote.save()
        generate_quote_pdf(quote)


        return redirect(
            'quotes:quote_list'
        )


    return render(

        request,

        'quotes/form.html',

        {

            'form':form,

            'formset':formset

        }

    )




@login_required(login_url='accounts:login')
def update_quote(request, pk):
    if request.user.role not in ['owner']:
        return HttpResponseForbidden("Vous n'avez pas la permission de modifier un devis.")


    quote = get_object_or_404(Quote, pk=pk)

    if request.method == 'POST':

        form = QuoteForm(request.POST, instance=quote)
        formset = QuoteItemFormSet(request.POST, instance=quote, prefix='items')

        if form.is_valid() and formset.is_valid():
            quote = form.save(commit=False)
            quote.user = request.user
            quote.save()

            formset.save()

            # recalcul total APRÈS save
            quote.recalc_total()

            return redirect('quotes:quote_list')

    else:
        form = QuoteForm(instance=quote)
        formset = QuoteItemFormSet(instance=quote, prefix='items')

    return render(request, 'quotes/form.html', {
        'form': form,
        'formset': formset,
        'quote': quote
    })






def generate_quote_pdf(quote):

    logo_path = os.path.join(

        settings.BASE_DIR,

        "static",

        "images",

        "sonikara_elec_logo.png"

    )


    logo_path = (

        f"file://{logo_path}"

    )


    context = {

        'quote': quote,

        'logo_path': logo_path,

    }


    html = (

        render_to_string(

            'quotes/quote_pdf.html',

            context

        )

    )


    pdf = (

        HTML(

            string=html,

            base_url=settings.BASE_DIR

        )

        .write_pdf()

    )


    filename = (

        f"devis_{quote.reference}.pdf"

    )


    quote.pdf.save(

        filename,

        ContentFile(pdf),

        save=True

    )


    return quote