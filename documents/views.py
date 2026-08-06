from django.shortcuts import render, redirect, get_object_or_404

from .forms import DocumentForm
from .models import Document
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, FileResponse, Http404

from django.utils import timezone
from django.core.paginator import Paginator

from .services import generate_pdf
from sonikaraelectrostock import tools


@login_required(login_url='accounts:login')
def document_pdf(request, pk):
    document = get_object_or_404(Document, pk=pk, company=request.user.company)
    if not document.pdf:
        raise Http404()

    return FileResponse(
        document.pdf.open("rb"),
        content_type="application/pdf"
    )





@login_required(login_url='accounts:login')
def create_document(request):

    form = DocumentForm(request.POST or None)
    if form.is_valid():
        document = form.save(commit=False)
        document.company = request.user.company
        document.generated_by = request.user
        document.reference = tools.generate_reference('DOC', Document)
        document.save()

        generate_pdf(document, company=request.user.company)

        return redirect('documents:list')

    return render(request, 'documents/form.html', {'form':form})






@login_required(login_url='accounts:login')
def document_list(request):

    documents = (
        Document.objects.for_company(request.user.company)
        .filter(is_deleted=False)
        .select_related(
            'purchase',
            'sale',
            'generated_by'
        )
        .order_by('-created_at')
    )

    paginator = Paginator(documents, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'documents': page_obj,
        'page_obj': page_obj,
    }

    return render(request, 'documents/list.html', context)



@login_required(login_url='accounts:login')
def delete_document(request, pk):

    if request.user.role not in ['owner']:
        return HttpResponseForbidden(
            "Vous n'avez pas la permission de supprimer un document."
        )

    document = (
        get_object_or_404(
            Document,
            company=request.user.company,
            id=pk,
            is_deleted=False
        )
    )

    document.is_deleted = True
    document.save(update_fields=['is_deleted'])

    return redirect('documents:list')