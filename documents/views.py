from django.shortcuts import render, redirect, get_object_or_404

from .forms import DocumentForm
from .models import Document
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from django.utils import timezone

from .services import generate_pdf





# Generation of reference number
def generate_reference():

    """Generation of reference number

    Returns:
        str: reference number
    """

    now = timezone.now()

    prefix = (
        f"DOC-"
        f"{now:%Y%m}"
    )

    count = Document.objects.count() + 1

    return (

        f"{prefix}"

        f"-{count:04d}"
    )






@login_required(login_url='accounts:login')
def create_document(request):

    form = (

        DocumentForm(

            request.POST

            or None

        )

    )


    if form.is_valid():

        document = (

            form.save(
                commit=False
            )

        )

        document.generated_by = request.user
        document.reference = generate_reference()

        document.save()
        generate_pdf(document)

        return redirect(

            'documents:list'

        )


    return render(

        request,

        'documents/form.html',

        {

            'form':form

        }

    )






@login_required(login_url='accounts:login')
def document_list(
    request
):

    documents = (

        Document.objects
        .filter(
            is_deleted=False
        )
        .select_related(

            'purchase',

            'sale',

            'generated_by'

        )

        .order_by(

            '-created_at'

        )

    )

    return render(request, 'documents/list.html', {'documents':documents})



@login_required(login_url='accounts:login')
def delete_document(request, pk):

    if request.user.role not in ['owner']:
        return HttpResponseForbidden(
            "Vous n'avez pas la permission de supprimer un document."
        )

    document = (
        get_object_or_404(
            Document,
            id=pk,
            is_deleted=False
        )
    )

    document.is_deleted = True

    document.save(
        update_fields=[
            'is_deleted'
        ]
    )

    return redirect('documents:list')