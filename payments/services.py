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


def validate_payment_amount(payment_amount, remaining_amount):
    if payment_amount <= 0:
        return "Le montant doit être supérieur à 0."

    if payment_amount > remaining_amount:
        return "Montant trop élevé."

    return None