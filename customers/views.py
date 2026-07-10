from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import Customer
from .forms import CustomerForm
from .serializers import CustomerSearchSerializer, CustomerCreateSerializer
from django.db.models import Q
from django.core.paginator import Paginator

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def customer_search_api(request):
    query = request.GET.get('q', '').strip()

    if len(query) < 1:
        return Response({'results': []})

    customers = (
        Customer.objects
        .filter(is_deleted=False)
        .filter(
            Q(phone__icontains=query) |
            Q(name__icontains=query)
        )
        .order_by('name')[:20]
    )

    serializer = CustomerSearchSerializer(customers, many=True)
    return Response({'results': serializer.data})



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_customer_api(request):
    serializer = CustomerCreateSerializer(data=request.data)
    if serializer.is_valid():
        customer = serializer.save()
        return Response({
                'success': True,
                'id': customer.id,
                'name': customer.name,
                'phone': customer.phone,
            })

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@login_required(login_url='accounts:login')
def customer_list(request):

    customers = Customer.objects.filter(is_deleted=False).order_by('-created_at')

    paginator = Paginator(customers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context =  {
        'customers': page_obj, 
        'page_obj': page_obj, 
    }

    return render(request, 'customers/list.html', context)



@login_required(login_url='accounts:login')
def customer_create(request):
    if request.user.role not in ['owner']:
        return HttpResponseForbidden("Vous n'avez pas la permission d'ajouter un client.")
    form = CustomerForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('customers:list')

    return render(request, 'customers/form.html', {'form':form})




# mise à jour d'un client
@login_required(login_url='accounts:login')
def update_customer(request, pk):
    if request.user.role not in ['owner']:
        return HttpResponseForbidden("Vous n'avez pas la permission à mettre à jour le client.")

    customer = get_object_or_404(Customer, id=pk)
    form = CustomerForm(request.POST or None, instance=customer)
    if form.is_valid():
        form.save()
        return redirect('customers:list')
    return render(request, 'customers/form.html', {'form':form})





@login_required(login_url='accounts:login')
def delete_customer(request, pk):
    if request.user.role not in ['owner']:
        return HttpResponseForbidden("Vous n'avez pas la permission de supprimer un client.")
    customer = get_object_or_404(Customer, id=pk)
    customer.is_deleted = True
    customer.save()
    return redirect('customers:list')