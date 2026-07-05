from django.urls import path

from .views import *

app_name = 'quotes'

urlpatterns = [
    path('', quote_list, name='quote_list'),
    path('create/', create_quote, name='create_quote'),
    path('<int:pk>/update/', update_quote, name='update_quote'),
    path('generate/pdf', generate_quote_pdf, name='generate_quote_pdf'),
    path('<int:pk>/print/', print_quote, name='print_quote'),
]