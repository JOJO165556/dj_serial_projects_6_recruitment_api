from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import CandidateProfile
from .serializers import CandidateProfileSerializer
from drf_spectacular.utils import extend_schema_view, extend_schema

@extend_schema_view(
    list=extend_schema(summary="Profils Candidats", description="Le candidat voit son propre profil. Le recruteur accède à toute la base de profils.", tags=["Candidats"]),
    create=extend_schema(summary="Créer son profil", tags=["Candidats"]),
    retrieve=extend_schema(summary="Détail du profil", tags=["Candidats"]),
    update=extend_schema(summary="Mettre à jour son profil", tags=["Candidats"]),
    partial_update=extend_schema(summary="Mettre à jour partiellement", tags=["Candidats"]),
    destroy=extend_schema(summary="Supprimer son profil", tags=["Candidats"])
)
class CandidateProfileViewSet(viewsets.ModelViewSet):
    serializer_class = CandidateProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Chaque user ne voit que son profil, sauf les recruteurs qui voient l'ensemble des candidats.
        """
        user = self.request.user
        if getattr(user, "role", None) == "RECRUITER":
            return CandidateProfile.objects.all()
        return CandidateProfile.objects.filter(user=user)