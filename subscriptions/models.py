from django.db import models
from django.utils import timezone
import uuid


class Company(models.Model):

    name = models.CharField(max_length=200)

    owner = models.OneToOneField(
        "accounts.CustomUser",
        on_delete=models.CASCADE,
        related_name="owned_company"
    )

    subdomain = models.SlugField(unique=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    reference = models.CharField(max_length=150, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
    


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    monthly_price = models.PositiveIntegerField()
    installation_fee = models.PositiveIntegerField(default=0)
    reference = models.CharField(max_length=150, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name



class Subscription(models.Model):

    STATUS = [
        ("trial", "Essai"),
        ("active", "Actif"),
        ("expired", "Expiré"),
        ("suspended", "Suspendu"),
    ]

    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name="subscription")
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS,  default="trial")
    trial = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    reference = models.CharField(max_length=150, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_valid(self):
        return self.status in ["trial", "active"] and self.end_date >= timezone.now().date()

    @property
    def remaining_days(self):
        return max(0, (self.end_date - timezone.now().date()).days)

    def __str__(self):
        return self.company.name



class Payment(models.Model):

    METHOD = [
        ("cash", "Espèces"),
        ("bank", "Banque"),
        ("orange", "Orange Money"),
        ("wave", "Wave"),
        ("moov", "Moov"),
        ("other", "Autre"),
    ]

    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name="payments")
    amount = models.PositiveIntegerField()
    payment_date = models.DateField()
    period_month = models.PositiveIntegerField()
    method = models.CharField(max_length=20, choices=METHOD)
    reference = models.CharField(max_length=150, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subscription.company} - {self.amount}"
