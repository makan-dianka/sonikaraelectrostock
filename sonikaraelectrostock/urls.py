from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


app_name = "accounts"
urlpatterns = [
    path('', include("dashboard.urls")),
    path('sonikaraelec/', admin.site.urls),
    path('accounts/', include("accounts.urls")),
    path('stores/', include("stores.urls")),
    path('products/', include("products.urls")),
    path('stocks/', include("stocks.urls")),
    path('suppliers/', include("suppliers.urls")),
    path('purchases/', include("purchases.urls")),
    path('customers/', include("customers.urls")),
    path('sales/', include("sales.urls")),
    path('payments/', include("payments.urls")),
    path('documents/', include("documents.urls")),
    path('quotes/', include("quotes.urls")),
    path('credits/', include("credits.urls")),
    path('expenses/', include("expenses.urls")),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
