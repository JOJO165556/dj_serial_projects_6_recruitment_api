from django.db import models
from apps.core.models import TimeStampedModel

class CandidateProfile(TimeStampedModel):
    """
    Profil métier du candidat.
    """

    user = models.OneToOneField(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="candidate_profile"
    )

    cv = models.FileField(
        upload_to="cvs/",
        null=True,
        blank=True
    )

    skills = models.TextField(blank=True)
    experience = models.TextField(blank=True)

    def __str__(self):
        return self.user.email