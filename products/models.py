from django.db import models
from sonikaraelectrostock.models import TimeStampedModel


class Category(TimeStampedModel):

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name



class Marque(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    class Meta:
        verbose_name_plural = "Marques"

    def __str__(self):
        return self.name



class Product(TimeStampedModel):

    name = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    marque = models.ForeignKey(
        Marque, on_delete=models.PROTECT, null=True, blank=True, related_name='products'
    )
    reference = models.CharField(max_length=100, unique=True)
    purchase_price = models.IntegerField(null=True, blank=True)
    sale_price = models.IntegerField(null=True, blank=True)
    description = models.TextField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to="products/", blank=True)
    is_deleted = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.name