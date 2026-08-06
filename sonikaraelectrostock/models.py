from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class CompanyManager(models.Manager):
    def for_company(self, company):
        return self.filter(company=company)


class CompanyOwnedModel(models.Model):
    company = models.ForeignKey(
        "subscriptions.Company",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="%(class)ss"
    )

    objects = CompanyManager()

    class Meta:
        abstract = True