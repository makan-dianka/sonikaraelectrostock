from django.db import models
from sonikaraelectrostock.models import TimeStampedModel
from django.utils import timezone


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
        null=True,
        unique=True
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

    def update_total(self):
        total = sum(item.quantity * item.unit_price for item in self.items.all())
        self.total_amount = total
        self.save()


    def can_change_to(self, new_status):

        transitions = {
            'draft': [
                'received',
                'cancelled'
            ],

            'received': [],

            'cancelled': []
        }

        return (new_status in transitions[self.status])





    def generate_invoice_number(self):
        """genere invoice number

        Returns:
            str: invoice number
        """

        today = timezone.now()


        prefix = (f"FACT-ACH-" f"{today:%Y%m}-")

        last = (
            Purchase.objects.filter(
                invoice_number__startswith=prefix
            ).order_by(
                '-invoice_number'
            ).first()
        )

        if last:

            try:
                seq = int(last.invoice_number.split('-')[-1]) + 1
            except:
                seq = 1
        else:
            seq = 1
        return (f"{prefix}" f"{seq:04d}")



    def save(self, *args, **kwargs):

        if not self.invoice_number:
            self.invoice_number = self.generate_invoice_number()
        super().save(*args, **kwargs)






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