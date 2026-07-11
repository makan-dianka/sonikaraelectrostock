from customers.models import Customer
from expenses.models import Expense
from suppliers.models import Supplier
from products.models import Product
from credits.models import Credit

from customers.serializers import CustomerSearchSerializer
from suppliers.serializers import SupplierSearchSerializer
from products.serializers import ProductSearchSerializer
from expenses.serializers import ExpenseSearchSerializer
from credits.serializers import CreditSearchSerializer

SEARCH_CONFIG = {

    "customers": {
        "model": Customer,
        "serializer": CustomerSearchSerializer,
        "search_fields": ["name", "phone"],
        "order_by": "name",
    },

    "suppliers": {
        "model": Supplier,
        "serializer": SupplierSearchSerializer,
        "search_fields": ["name", "phone"],
        "order_by": "name",
    },

    "products": {
        "model": Product,
        "serializer": ProductSearchSerializer,
        "search_fields": ["name", "reference"],
        "order_by": "name",
    },

    "expenses": {
        "model": Expense,
        "serializer": ExpenseSearchSerializer,
        "search_fields": ["reference", "category__name"],
        "order_by": "category__name",
    },

    "credits": {
        "model": Credit,
        "serializer": CreditSearchSerializer,
        "search_fields": ["reference", "customer__name"],
        "order_by": "customer__name",
    },

}