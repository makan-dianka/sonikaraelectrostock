from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views


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
    path('subscriptions/', include("subscriptions.urls")),


    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/passwords/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/passwords/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/passwords/password_reset_complete.html'), name='password_reset_complete'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
