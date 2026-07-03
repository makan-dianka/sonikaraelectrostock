from stocks.models import Stock


def receive_purchase(purchase):
    """
    Mise à jour l'état de l'achat, 
    création et mise à jour du stock,
    mise à jour du prix d'achat de produit

    Args:
        purchase (_type_): l'instance du purchase
    """

    if purchase.status != 'draft':
        raise Exception(
            "Achat déjà traité."
        )


    for item in purchase.items.all():
        stock, created = Stock.objects.get_or_create(
            store=purchase.store,
            product=item.product,
            defaults={'quantity':0}
        )

        # MAJ stock
        # après l'achat, on augmente le stock
        stock.quantity += item.quantity
        stock.save()

        # MAJ PRIX ACHAT
        # on met à jour le prix 
        # d'achat de chaque produit
        product = item.product
        product.purchase_price = item.unit_price
        product.save(update_fields=['purchase_price'])

    # on met à jour l'état de l'achat
    # à received (receptionné)
    purchase.status = 'received'
    purchase.save()




def cancel_purchase(purchase):
    """
    Mise à jour l'état de l'achat, 
    supprimer le montant qui a été augmenté lors de création
    de l'achat

    Args:
        purchase (_type_): l'instance du purchase

    """

    if purchase.status != 'draft':
        raise Exception(
            "Achat déjà traité."
        )


    # on met à jour l'état de l'achat
    # à cancelled (annulé)
    purchase.status = 'cancelled'
    purchase.save()