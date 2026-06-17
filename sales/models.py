from django.db import models
from sonikaraelectrostock.models import TimeStampedModel


class Sale(TimeStampedModel):

    STATUS = [

        ('draft', 'Brouillon'),

        ('validated', 'Validée'),

        ('cancelled', 'Annulée')

    ]



    reference = models.CharField(max_length=100, unique=True)
    customer = models.ForeignKey(
        "customers.Customer",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    store = models.ForeignKey(
        "stores.Store",
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    total = models.IntegerField(default=0)

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='draft'
    )

    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('unpaid', 'Non payé'),
            ('partial', 'Partiel'),
            ('paid', 'Payé')
        ],
        default='unpaid'
    )


    def __str__(self):
        return self.reference


    @property
    def paid_amount(self):
        return (self.payments.aggregate(total=models.Sum('amount')) ['total'] or 0)


    @property
    def remaining_amount(self):
        return (self.total - self.paid_amount)








class SaleItem(models.Model):

    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField()

    unit_price = models.IntegerField()

    subtotal = models.IntegerField()