from django.db import transaction

from stocks.models import Stock


@transaction.atomic
def validate_sale(sale):

    if sale.status not in ['draft', 'cancelled']:
        raise Exception("Vente déjà traitée.")


    # Vérification
    for item in sale.items.all():

        try:
            stock = Stock.objects.get(store=sale.store, product=item.product)

        except Stock.DoesNotExist:

            raise Exception(

                f"Le produit "

                f"{item.product}"

                f" n'existe pas "

                f"dans le stock."

            )


        if stock.quantity < item.quantity:
            raise Exception(f"Stock insuffisant : " f"{item.product}")


    # Décrément
    for item in sale.items.all():

        stock = Stock.objects.get(store=sale.store, product=item.product)

        stock.quantity -= item.quantity

        stock.save()


    sale.status = 'validated'
    sale.save()






@transaction.atomic
def cancel_sale(sale):

    if sale.status not in ['draft', 'validated']:
        raise Exception("Vente déjà annulé.")


    # Vérification
    for item in sale.items.all():

        try:
            stock = Stock.objects.get(store=sale.store, product=item.product)

        except Stock.DoesNotExist:

            raise Exception(

                f"Le produit "

                f"{item.product}"

                f" n'existe pas "

                f"dans le stock."

            )


    # incrementer le stock
    for item in sale.items.all():

        stock = Stock.objects.get(store=sale.store, product=item.product)

        stock.quantity += item.quantity

        stock.save()


    sale.status = 'cancelled'
    sale.save()