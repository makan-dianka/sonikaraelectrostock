from django.db import models
from sonikaraelectrostock.models import TimeStampedModel


class Payment(TimeStampedModel):

    METHOD = [
        ('cash', 'Espèces'),
        ('vir', 'Virement'),
        ('cheque', 'Chèque'),
        ('om', 'Orange Money'),
    ]


    purchase = models.ForeignKey(
        'purchases.Purchase',
        on_delete=models.CASCADE,
        related_name='payments',
        null=True,
        blank=True
    )

    sale = models.ForeignKey(
        'sales.Sale',
        on_delete=models.CASCADE,
        related_name='payments',
        null=True,
        blank=True
    )

    amount = models.IntegerField()

    payment_method = models.CharField(max_length=20, choices=METHOD)

    reference = models.CharField(max_length=150, blank=True, null=True)

    notes = models.TextField(blank=True)

    created_by = models.ForeignKey('accounts.CustomUser', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        if self.sale:
            return self.sale.reference
        return self.purchase.reference
    
    def get_reference(self):
        if self.sale:
            return self.sale.reference
        if self.purchase:
            return self.purchase.reference
        return "-"
    
    def get_remaining(self):
        if self.sale:
            return self.sale.remaining_amount
        if self.purchase:
            return self.purchase.remaining_amount
