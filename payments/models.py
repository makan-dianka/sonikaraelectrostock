from django.db import models
from sonikaraelectrostock.models import TimeStampedModel


class Payment(TimeStampedModel):

    METHOD = [
        ('cash', 'Espèces'),
        ('vir', 'Virement'),
        ('cheque', 'Chèque'),
        ('om', 'Orange Money'),
        ('credit', 'Crédit'),
    ]


    sale = models.ForeignKey('sales.Sale', on_delete=models.CASCADE, related_name='payments')

    amount = models.IntegerField()

    payment_method = models.CharField(max_length=20, choices=METHOD)

    reference = models.CharField(max_length=150, blank=True, null=True)

    notes = models.TextField(blank=True)

    created_by = models.ForeignKey('accounts.CustomUser', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.sale.reference