from django.db import models
from apps.core.models import TimeStampedModel

class JobOffer(TimeStampedModel):

    class JobType(models.TextChoices):
        FULL_TIME = "FULL_TIME"
        PART_TIME = "PART_TIME"
        INTERNSHIP = "INTERNSHIP"
        CONTRACT = "CONTRACT"

    title = models.CharField(max_length=255)
    description = models.TextField()

    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.CASCADE,
        related_name="jobs"
    )

    location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=20, choices=JobType.choices) #type: ignore

    salary_min = models.IntegerField(null=True, blank=True)
    salary_max = models.IntegerField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
