from django.db import models
from apps.core.models import TimeStampedModel

class Notification(TimeStampedModel):
    """
    Notification système simple.
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