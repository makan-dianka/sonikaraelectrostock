from django.core.management.base import BaseCommand

from subscriptions.models import Company

from products.models import Product
from customers.models import Customer
from sales.models import Sale
from credits.models import CreditPayment, Credit
from documents.models import Document
from expenses.models import ExpenseCategory, Expense
from payments.models import Payment
from products.models import Product, Marque, Category
from purchases.models import Purchase
from quotes.models import Quote
from stocks.models import Stock
from stores.models import Store
from subscriptions.models import Subscription
from suppliers.models import Supplier
from accounts.models import CustomUser

import os


class Command(BaseCommand):

    help = "Associe les anciennes données à une entreprise"


    def handle(self, *args, **kwargs):

        try:
            company = Company.objects.get(uuid=os.getenv("COMPANY_UUID"))
        except Company.DoesNotExist:
            self.stdout.write(self.style.ERROR("Entreprise introuvable"))
            return

        Product.objects.filter(
            company=None
        ).update(company=company)

        Customer.objects.filter(
            company=None
        ).update(company=company)

        Sale.objects.filter(
            company=None
        ).update(company=company)

        CreditPayment.objects.filter(
            company=None
        ).update(company=company)

        Credit.objects.filter(
            company=None
        ).update(company=company)

        Document.objects.filter(
            company=None
        ).update(company=company)

        ExpenseCategory.objects.filter(
            company=None
        ).update(company=company)

        Expense.objects.filter(
            company=None
        ).update(company=company)

        Payment.objects.filter(
            company=None
        ).update(company=company)

        Purchase.objects.filter(
            company=None
        ).update(company=company)

        Quote.objects.filter(
            company=None
        ).update(company=company)

        Stock.objects.filter(
            company=None
        ).update(company=company)

        Store.objects.filter(
            company=None
        ).update(company=company)

        Subscription.objects.filter(
            company=None
        ).update(company=company)

        Supplier.objects.filter(
            company=None
        ).update(company=company)

        CustomUser.objects.filter(
            company=None
        ).update(company=company)

        Marque.objects.filter(
            company=None
        ).update(company=company)

        Category.objects.filter(
            company=None
        ).update(company=company)


        self.stdout.write(
            self.style.SUCCESS(
                "Données associées avec succès"
            )
        )


# Taper cette commande au terminal pour l'exécuter :
# python manage.py assign_company