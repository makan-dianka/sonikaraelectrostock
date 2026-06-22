from django.db import models
from sonikaraelectrostock.models import TimeStampedModel


class Credit(TimeStampedModel):

    PENDING = "pending"
    PARTIAL = "partial"
    PAID = "paid"
    OVERDUE = "overdue"

    STATUS_CHOICES = [
        (PENDING, "En attente"),
        (PARTIAL, "Partiellement remboursé"),
        (PAID, "Remboursé"),
        (OVERDUE, "En retard"),
    ]
    reference = models.CharField(max_length=100, unique=True)

    customer = models.ForeignKey(
        "customers.Customer",
        on_delete=models.CASCADE,
        related_name="credits"
    )

    user = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    store = models.ForeignKey(
        "stores.Store",
        on_delete=models.CASCADE
    )

    amount = models.IntegerField()

    interest_rate = models.IntegerField(default=0)

    due_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING
    )

    note = models.TextField(blank=True)
    is_deleted = models.BooleanField(default=False, blank=True, null=True)


    def __str__(self):
        return self.reference

    @property
    def total_paid(self):
        return sum(p.amount for p in self.payments.all())

    @property
    def remaining(self):
        return self.total_with_interest_rate_amount - self.total_paid


    @property
    def interest_rate_amount(self):
        return round(self.amount * self.interest_rate / 100)


    @property
    def total_with_interest_rate_amount(self):
        return self.amount + self.interest_rate_amount






class CreditPayment(TimeStampedModel):

    reference = models.CharField(max_length=100, unique=True, null=True, blank=True)

    credit = models.ForeignKey(
        Credit,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    amount = models.IntegerField()

    payment_method = models.CharField(
        max_length=20,
        choices=[
            ("cash", "Espèces"),
            ("virement", "Virement bancaire"),
            ("cheque", "Chèque"),
            ("Om", "Orange money"),
        ],
        default="cash"
    )

    note = models.TextField(blank=True)
    is_deleted = models.BooleanField(default=False, blank=True, null=True)