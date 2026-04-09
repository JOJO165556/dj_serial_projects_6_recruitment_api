from django.db import models
from apps.core.models import TimeStampedModel

class Notification(TimeStampedModel):
    """
    Modèle asynchrone stockant l'historique des alertes (Notifications).
    Il est peuplé via les `services.py` de l'application métier pour alerter
    le candidat ou le recruteur des événements critiques.
    """

    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    title = models.CharField(max_length=255)
    message = models.TextField()

    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.title