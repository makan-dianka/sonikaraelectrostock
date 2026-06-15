from django.db import models
from sonikaraelectrostock.models import TimeStampedModel


class Purchase(TimeStampedModel):

    STATUS = [
        ('draft', 'Brouillon'),
        ('received', 'Réceptionné'),
        ('cancelled', 'Annulé'),
    ]

    supplier = models.ForeignKey(
        'suppliers.Supplier',
        on_delete=models.PROTECT,
        related_name='purchases'
    )

    store = models.ForeignKey(
        'stores.Store',
        on_delete=models.PROTECT,
        related_name='purchases'
    )

    invoice_number = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    purchase_date = models.DateField()

    total_amount = models.IntegerField(default=0)

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='draft'
    )

    created_by = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.SET_NULL,
        null=True
    )

    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Achat #{self.id}"
    





class PurchaseItem(TimeStampedModel):

    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        'products.Product',
        on_delete=models.PROTECT
    )

    quantity = models.IntegerField()

    unit_price = models.IntegerField()

    total = models.IntegerField()

    def save(self, *args, **kwargs):
        self.total = (self.quantity * self.unit_price)
        super().save(*args, **kwargs)