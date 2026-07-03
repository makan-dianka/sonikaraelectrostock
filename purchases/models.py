from django.db import models
from sonikaraelectrostock.models import TimeStampedModel
from sonikaraelectrostock.tools import generate_reference
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

    reference = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        unique=True
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

    purchase_date = models.DateField()

    total = models.IntegerField(default=0)

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
        return self.reference

    def update_total(self):
        total = sum(item.quantity * item.unit_price for item in self.items.all())
        self.total = total
        self.save()

    # pour recalculer le total après un update
    def recalc_total(self):
        total = sum(item.total for item in self.items.all())
        self.total = total
        self.save(update_fields=['total'])


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



    def save(self, *args, **kwargs):

        if not self.reference:
            self.reference = generate_reference('ACH', Purchase)
        super().save(*args, **kwargs)


    @property
    def paid_amount(self):
        return (self.payments.aggregate(total=models.Sum('amount'))['total'] or 0)


    @property
    def remaining_amount(self):
        return (self.total - self.paid_amount)






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