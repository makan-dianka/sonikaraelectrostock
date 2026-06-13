from django.db import models
from sonikaraelectrostock.models import TimeStampedModel


class Store(TimeStampedModel):
    name = models.CharField(max_length=150)

    phone = models.CharField(
        max_length=30,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.name