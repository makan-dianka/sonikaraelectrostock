from .models import Payment


def update_payment_status(sale):

    paid = sale.paid_amount

    if paid <= 0:
        sale.payment_status = 'unpaid'
    elif paid < sale.total:
        sale.payment_status = 'partial'
    else:
        sale.payment_status = 'paid'

    sale.save()