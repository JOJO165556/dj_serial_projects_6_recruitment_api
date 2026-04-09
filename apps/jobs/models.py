from django.db import models
from apps.core.models import TimeStampedModel

class JobOffer(TimeStampedModel):
    """
    Entité au coeur de l'application : l'Offre d'Emploi.
    Reliée à une entreprise (Company). 
    Filtre automatiquement les postulations si is_active=False.
    """
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

class JobView(TimeStampedModel):
    """
    Modèle d'analytics enregistrant les clics/vues d'une offre d'emploi.
    Permet de calculer le taux de conversion (Candidatures / Vues).
    """

    job = models.ForeignKey(
        "jobs.JobOffer",
        on_delete=models.CASCADE,
        related_name="views"
    )

    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )