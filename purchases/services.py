from stocks.models import Stock


def receive_purchase(purchase):

    for item in purchase.items.all():
        stock, created = (
            Stock.objects.get_or_create(
                product=item.product,
                store=purchase.store,
                defaults={'quantity':0}
            )
        )

        stock.quantity += (item.quantity)
        stock.save()

    purchase.status = ('received')
    purchase.save()