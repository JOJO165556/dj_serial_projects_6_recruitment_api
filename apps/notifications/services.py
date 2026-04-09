from .models import Notification
import logging

logger = logging.getLogger(__name__)

def create_notification(user, title, message):
    """
    Crée une notif pour un user.
    """

    notification = Notification.objects.create(
        user=user,
        title=title,
        message=message
    )
    logger.info(f"Notification sent to {user.email}: {title}")
    return notification
