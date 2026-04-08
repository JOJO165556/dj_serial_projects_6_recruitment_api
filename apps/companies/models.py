from django.db import models
from apps.core.models import TimeStampedModel

class Company(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    owner = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="companies",
    )

    website = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name