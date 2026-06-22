from django.db import models
from sonikaraelectrostock.models import TimeStampedModel


class Quote(TimeStampedModel):

    reference = models.CharField(max_length=100, unique=True)

    customer = models.ForeignKey(
        "customers.Customer",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    user = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ('draft','Brouillon'),
            ('sent','Envoyé'),
            ('accepted','Accepté'),
            ('rejected','Refusé')
        ],
        default='draft'
    )

    store = models.ForeignKey("stores.Store", on_delete=models.CASCADE)
    labor_cost = models.IntegerField(default=0, verbose_name="Coût main d'œuvre")
    vat_rate = models.IntegerField(default=18)
    reduction = models.IntegerField(default=10)
    delivery_fee = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    total = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False, blank=True, null=True)

    pdf = models.FileField(
        upload_to='quotes/',
        blank=True,
        null=True
    )


    def __str__(self):
        return self.reference


    @property
    def vat_amount(self):
        return round(self.total * self.vat_rate / 100)
    
    def reduction_amount(self):
        return int(self.total_ttc / 100 * self.reduction)


    def total_amount(self):
        return self.total_ttc - self.reduction_amount()


    @property
    def total_ttc(self):
        return self.total + self.labor_cost + self.vat_amount + self.delivery_fee





class QuoteItem(models.Model):

    quote = models.ForeignKey(
        Quote,
        related_name='items',
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField()

    unit_price = models.IntegerField()

    subtotal = models.IntegerField()