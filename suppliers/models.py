from django.db import models
from sonikaraelectrostock.models import CompanyOwnedModel, TimeStampedModel


class Supplier(TimeStampedModel, CompanyOwnedModel):

    name = models.CharField(max_length=250)
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name