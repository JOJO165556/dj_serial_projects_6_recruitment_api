from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Notification
from .serializers import NotificationSerializer
from drf_spectacular.utils import extend_schema_view, extend_schema

@extend_schema_view(
    list=extend_schema(summary="Mes notifications", description="Historique des alertes pour l'utilisateur courant.", tags=["Notifications"]),
    create=extend_schema(summary="Créer une notification manuelle", tags=["Notifications"]),
    retrieve=extend_schema(summary="Voir une notification", tags=["Notifications"]),
    update=extend_schema(summary="Modifier entièrement", tags=["Notifications"]),
    partial_update=extend_schema(summary="Marquer comme lu", tags=["Notifications"]),
    destroy=extend_schema(summary="Supprimer la notification", tags=["Notifications"])
)
class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Chaque user ne voit que ses notifs.
        """

        return Notification.objects.filter(user=self.request.user)