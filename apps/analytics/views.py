from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .services import recruiter_stats, candidate_stats

class AnalyticsView(APIView):
    """
    Retourne les stats selon le rôle de user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role == "RECRUITER":
            data = recruiter_stats(user)

        elif user.role == "CANDIDATE":
            data = candidate_stats(user)

        else:
            data = {}

        return Response(data)