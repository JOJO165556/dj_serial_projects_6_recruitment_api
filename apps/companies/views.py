from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.accounts.permissions import IsRecruiterUser
from .models import Company
from .serializers import CompanySerializer
from drf_spectacular.utils import extend_schema_view, extend_schema

@extend_schema_view(
    list=extend_schema(summary="Lister mes entreprises", description="Renvoie les entreprises dont l'utilisateur métier est propriétaire.", tags=["Entreprises"]),
    create=extend_schema(summary="Créer une entreprise", tags=["Entreprises"]),
    retrieve=extend_schema(summary="Détails de l'entreprise", tags=["Entreprises"]),
    update=extend_schema(summary="Modifier totalement l'entreprise", tags=["Entreprises"]),
    partial_update=extend_schema(summary="Modifier partiellement l'entreprise", tags=["Entreprises"]),
    destroy=extend_schema(summary="Supprimer l'entreprise", tags=["Entreprises"])
)
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsRecruiterUser]

    def get_queryset(self):
        return Company.objects.filter(owner=self.request.user)
