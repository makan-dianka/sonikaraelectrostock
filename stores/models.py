from django.db import models
from sonikaraelectrostock.models import CompanyOwnedModel, TimeStampedModel


class Store(TimeStampedModel, CompanyOwnedModel):
    name = models.CharField(max_length=150)

    phone = models.CharField(
        max_length=30,
        blank=True
    )

    address = models.TextField(blank=True)
    is_deleted = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.name