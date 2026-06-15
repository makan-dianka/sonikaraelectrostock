from django.db import models
from sonikaraelectrostock.models import TimeStampedModel

class Stock(TimeStampedModel):

    store = models.ForeignKey("stores.Store", on_delete=models.CASCADE, related_name='stocks')
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name='stocks')
    quantity = models.IntegerField(default=0)
    alert_threshold = models.IntegerField(default=10)

    class Meta:
        unique_together = ("store", "product")
