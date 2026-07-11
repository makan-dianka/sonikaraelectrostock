from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from common.pagination import paginate_queryset
from suppliers.serializers import SupplierCreateSerializer, SupplierSearchSerializer

from .models import Supplier
from .forms import SupplierForm

from django.db.models import Q

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

import logging

logger = logging.getLogger('info_log')


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_supplier_api(request):
    serializer = SupplierCreateSerializer(data=request.data)
    if serializer.is_valid():
        supplier = serializer.save()
        return Response({
            "id": supplier.id,
            "name": supplier.name,
            "phone": supplier.phone,
        })
    return Response(serializer.errors, status=400)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def supplier_search_api(request):

    ##########################################
    ###############################################
    ############# API de recherche de fournisseurs #############
    ############# Recherche par nom ou téléphone #############
    ############# Retourne les 20 premiers résultats #############
    ############# Exemple d'URL: /api/suppliers/search/?q=John
    ##########################################

    alert="""

        !xxxxxx! ALERT !xxxxxx!
        Cette view est obsolète depuis [11/06/2026] et sera supprimée dans les prochaines versions. 
        Utilisez la views : search_api() dans common/search.py à la place.

    """
    logger.warning(alert)



    query = request.GET.get('q', '').strip()
    if len(query) < 1:
        return Response({'results': []})

    suppliers = (
        Supplier.objects
        .filter(is_deleted=False)
        .filter(
            Q(phone__icontains=query) |
            Q(name__icontains=query)
        )
        .order_by('name')[:20]
    )

    serializer = SupplierSearchSerializer(suppliers, many=True)
    return Response({'results': serializer.data})






@login_required(login_url='accounts:login')
def supplier_list(request):

    suppliers = Supplier.objects.filter(is_deleted=False).order_by('-created_at')

    page_obj = paginate_queryset(request, suppliers)

    context = {
        'suppliers': page_obj,
        'page_obj': page_obj,
    }

    return render(request, 'suppliers/list.html', context)



@login_required(login_url='accounts:login')
def supplier_create(request):
    if request.user.role not in ['owner']:
        return HttpResponseForbidden("Vous n'avez pas la permission d'ajouter un fournisseur.")
    form = SupplierForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('suppliers:list')

    return render(request, 'suppliers/form.html', {'form':form})




# mise à jour d'un fournisseur
@login_required(login_url='accounts:login')
def update_supplier(request, pk):
    if request.user.role not in ['owner']:
        return HttpResponseForbidden("Vous n'avez pas la permission à mettre à jour le fournisseur.")

    supplier = get_object_or_404(Supplier, id=pk)
    form = SupplierForm(request.POST or None, instance=supplier)
    if form.is_valid():
        form.save()
        return redirect('suppliers:list')
    return render(request, 'suppliers/form.html', {'form':form})





@login_required(login_url='accounts:login')
def delete_supplier(request, pk):
    if request.user.role not in ['owner']:
        return HttpResponseForbidden("Vous n'avez pas la permission de supprimer un fournisseur.")
    supplier = get_object_or_404(Supplier, id=pk)
    supplier.is_deleted = True
    supplier.save()
    return redirect('suppliers:list')