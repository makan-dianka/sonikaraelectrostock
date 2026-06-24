from .models import Payment


def update_payment_status(obj):

    paid = obj.paid_amount

    if paid <= 0:
        obj.payment_status = 'unpaid'
    elif paid < obj.total:
        obj.payment_status = 'partial'
    else:
        obj.payment_status = 'paid'

    obj.save()