from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.accounts.permissions import IsRecruiterUser, IsCandidateUser

from .models import Application
from .serializers import ApplicationSerializer
from .services import update_application_status

class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsCandidateUser()]
        if self.action == 'set_status':
            return [IsAuthenticated(), IsRecruiterUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user

        if user.role == "CANDIDATE":
            return Application.objects.filter(candidate=user)

        if user.role == "RECRUITER":
            return Application.objects.filter(
                job_offer__company__owner=user
            )

        return Application.objects.none()

    @action(detail=True, methods=["patch"])
    def set_status(self, request, pk=None):
        """
        Permet au recruteur de changer le status.
        """
        status = request.data.get("status")
        application = update_application_status(
            request.user,
            pk,
            status
        )

        return Response(ApplicationSerializer(application).data)