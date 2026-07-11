from customers.models import Customer
from expenses.models import Expense
from suppliers.models import Supplier
from products.models import Product
from credits.models import Credit
from payments.models import Payment

from customers.serializers import CustomerSearchSerializer
from suppliers.serializers import SupplierSearchSerializer
from products.serializers import ProductSearchSerializer
from expenses.serializers import ExpenseSearchSerializer
from credits.serializers import CreditSearchSerializer
from payments.serializers import PaymentSearchSerializer

SEARCH_CONFIG = {

    "customers": {
        "queryset": Customer.objects.filter(is_deleted=False),
        "serializer": CustomerSearchSerializer,
        "search_fields": ["name", "phone"],
        "order_by": "name",
    },

    "suppliers": {
        "queryset": Supplier.objects.filter(is_deleted=False),
        "serializer": SupplierSearchSerializer,
        "search_fields": ["name", "phone"],
        "order_by": "name",
    },

    "products": {
        "queryset": Product.objects.filter(is_deleted=False),
        "serializer": ProductSearchSerializer,
        "search_fields": ["name", "reference"],
        "order_by": "name",
    },

    "expenses": {
        "queryset": Expense.objects.filter(is_deleted=False),
        "serializer": ExpenseSearchSerializer,
        "search_fields": ["reference", "category__name"],
        "order_by": "category__name",
    },

    "credits": {
        "queryset": Credit.objects.filter(is_deleted=False),
        "serializer": CreditSearchSerializer,
        "search_fields": ["reference", "customer__name"],
        "order_by": "customer__name",
    },

    "payments": {
        "queryset": Payment.objects.all(),
        "serializer": PaymentSearchSerializer,
        "search_fields": ["reference"],
        "order_by": "reference",
    },

}