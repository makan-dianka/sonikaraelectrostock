from customers.models import Customer
from expenses.models import Expense
from expenses.serializers import ExpenseSearchSerializer
from suppliers.models import Supplier
from products.models import Product

from customers.serializers import CustomerSearchSerializer
from suppliers.serializers import SupplierSearchSerializer
from products.serializers import ProductSearchSerializer

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

}