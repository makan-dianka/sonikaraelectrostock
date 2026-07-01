from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Quote
from .forms import (
    QuoteForm,
    QuoteItemFormSet
)


from django.template.loader import render_to_string

from django.core.files.base import ContentFile

from weasyprint import HTML

from django.conf import settings
import os
from django.utils import timezone
from django.core.paginator import Paginator



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



# Generation of reference number
def generate_reference():

    """Generation of reference number

    Returns:
        str: reference number
    """

    now = timezone.now()

    prefix = (
        f"DEV-"
        f"{now:%Y%m%d}"
    )

    count = Quote.objects.count() + 1

    return (

        f"{prefix}"

        f"-{count:04d}"
    )



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

        quote.reference = generate_reference()

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