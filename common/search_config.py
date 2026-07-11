from customers.models import Customer
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

}