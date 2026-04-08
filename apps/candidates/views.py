from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import CandidateProfile
from .serializers import CandidateProfileSerializer

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