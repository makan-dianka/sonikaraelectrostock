from django.db import models

from sonikaraelectrostock.models import TimeStampedModel


class Document(TimeStampedModel):

    TYPE = [
        ('purchase_order', 'Bon achat'),
        ('delivery_note', 'Bon livraison'),
        ('invoice', 'Facture'),
    ]

    document_type = models.CharField(
        max_length=30,
        choices=TYPE
    )

    reference = models.CharField(
        max_length=100,
        unique=True
    )

    purchase = models.ForeignKey(
        'purchases.Purchase',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    sale = models.ForeignKey(
        'sales.Sale',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    generated_by = models.ForeignKey(
        'accounts.CustomUser',
        null=True,
        on_delete=models.SET_NULL
    )

    pdf = models.FileField(
        upload_to='documents/',
        blank=True,
        null=True
    )

    is_deleted = models.BooleanField(default=False, blank=True, null=True)