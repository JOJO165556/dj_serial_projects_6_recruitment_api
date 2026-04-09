from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .services import recruiter_stats, candidate_stats
from drf_spectacular.utils import extend_schema

class AnalyticsView(APIView):
    """
    Retourne les stats selon le rôle de user.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Tableau de bord (Statistiques)", description="Retourne un dictionnaire de KPIs. Le contenu varie automatiquement selon le Rôle (Candidate ou Recruiter).", tags=["Analytics"])
    def get(self, request):
        user = request.user

        if user.role == "RECRUITER":
            data = recruiter_stats(user)

        elif user.role == "CANDIDATE":
            data = candidate_stats(user)

        else:
            data = {}

        return Response(data)