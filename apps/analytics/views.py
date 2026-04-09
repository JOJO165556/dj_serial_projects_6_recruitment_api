from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers as drf_serializers

from .services import recruiter_stats, candidate_stats
from drf_spectacular.utils import extend_schema, inline_serializer

class AnalyticsView(APIView):
    """
    Retourne les stats selon le rôle de user.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Tableau de bord (Statistiques)",
        description="Retourne un dictionnaire de KPIs. Le contenu varie automatiquement selon le Rôle (Candidate ou Recruiter).",
        tags=["Analytics"],
        responses=inline_serializer(
            name="AnalyticsResponse",
            fields={
                "total_jobs": drf_serializers.IntegerField(required=False),
                "total_applications": drf_serializers.IntegerField(),
                "total_views": drf_serializers.IntegerField(required=False),
                "conversion_rate": drf_serializers.FloatField(required=False),
                "best_job": drf_serializers.CharField(required=False, allow_null=True),
                "accepted": drf_serializers.IntegerField(),
                "rejected": drf_serializers.IntegerField(),
                "in_progress": drf_serializers.IntegerField(required=False),
            }
        )
    )
    def get(self, request):
        user = request.user

        if user.role == "RECRUITER":
            data = recruiter_stats(user)

        elif user.role == "CANDIDATE":
            data = candidate_stats(user)

        else:
            data = {}

        return Response(data)