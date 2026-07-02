from django.db import models
from sonikaraelectrostock.models import TimeStampedModel


class ExpenseCategory(TimeStampedModel):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name




class Expense(TimeStampedModel):

    reference = models.CharField(max_length=100, unique=True)

    store = models.ForeignKey(
        "stores.Store",
        on_delete=models.CASCADE,
        related_name="expenses"
    )

    category = models.ForeignKey(
        ExpenseCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="expenses"
    )

    amount = models.IntegerField()

    description = models.TextField(blank=True)

    expense_date = models.DateField()

    payment_method = models.CharField(
        max_length=20,
        choices=[
            ('cash', 'Espèces'),
            ('vir', 'Virement'),
            ('cheque', 'Chèque'),
            ('om', 'Orange Money'),
        ],
        default="cash"
    )

    created_by = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.SET_NULL,
        null=True
    )

    is_deleted = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.reference
