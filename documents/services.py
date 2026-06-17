from io import BytesIO

from django.template.loader import render_to_string

from django.core.files.base import ContentFile

from weasyprint import HTML

from django.conf import settings
import os


def generate_pdf(document):
    logo_path = os.path.join(
        settings.BASE_DIR,
        "static",
        "images",
        "sonikara_elec_logo.png"
    )

    logo_path = f"file://{logo_path}"

    template = None

    context = {

        'document':document,
        'logo_path' : logo_path

    }


    if document.document_type == 'invoice':

        template = 'documents/pdf/invoice.html'

        context['sale'] = document.sale

    html = (

        render_to_string(

            template,

            context

        )

    )


    pdf = (

        HTML(
            string=html
        )

        .write_pdf()

    )


    filename = (

        f"{document.reference}.pdf"

    )


    document.pdf.save(

        filename,

        ContentFile(pdf),

        save=True

    )