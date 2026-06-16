from stocks.models import Stock


from stocks.models import Stock


def receive_purchase(purchase):

    if purchase.status != 'draft':
        raise Exception(
            "Achat déjà traité."
        )


    for item in purchase.items.all():

        stock, created = (

            Stock.objects.get_or_create(
                store=purchase.store,
                product=item.product,
                defaults={
                    'quantity':0
                }
            )
        )

        # MAJ stock
        stock.quantity += (
            item.quantity
        )
        stock.save()

        # MAJ PRIX ACHAT
        product = item.product
        product.purchase_price = item.unit_price
        product.save(update_fields=['purchase_price'])


    purchase.status = (
        'received'
    )

    purchase.save()