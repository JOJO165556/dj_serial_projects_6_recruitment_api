from .models import Notification

def create_notification(user, title, message):
    """
    Crée une notif pour un user.
    """

    return Notification.objects.create(
        user=user,
        title=title,
        message=message
    )