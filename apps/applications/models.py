from django.db import models

from apps.core.models import TimeStampedModel

class Application(TimeStampedModel):
    class Status(models.TextChoices):
        APPLIED = "APPLIED", "Applied"
        REVIEWED = "REVIEWED", "Reviewed"
        INTERVIEW = "INTERVIEW", "Interview"
        ACCEPTED = "ACCEPTED", "Accepted"
        REJECTED = "REJECTED", "Rejected"

    candidate = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="applications"
    )

    job_offer = models.ForeignKey(
        "jobs.JobOffer",
        on_delete=models.CASCADE,
        related_name="applications"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices, #type: ignore
        default=Status.APPLIED
    )

    cover_letter = models.FileField(
        upload_to="cover_letter/",
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.candidate.email} - {self.job_offer.title}"