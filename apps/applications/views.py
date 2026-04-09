from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.accounts.permissions import IsRecruiterUser, IsCandidateUser

from .models import Application
from .serializers import ApplicationSerializer
from .services import update_application_status
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse

@extend_schema_view(
    list=extend_schema(summary="Lister les candidatures", description="Candidats: Leurs candidatures. Recruteurs: Les candidatures reçues.", tags=["Candidatures"]),
    create=extend_schema(
        summary="Postuler à une offre", 
        description="Réservé aux profils candidats.", 
        tags=["Candidatures"],
        responses={
            201: OpenApiResponse(description="Candidature envoyée avec succès."),
            400: OpenApiResponse(description="Erreur de validation (Déjà postulé, offre inactive)."),
            403: OpenApiResponse(description="Accès refusé. Réservé aux Candidats.")
        }
    ),
    retrieve=extend_schema(summary="Détail de la candidature", tags=["Candidatures"]),
    update=extend_schema(summary="Mettre à jour la candidature", tags=["Candidatures"]),
    partial_update=extend_schema(summary="Modification partielle", tags=["Candidatures"]),
    destroy=extend_schema(summary="Retirer sa candidature", tags=["Candidatures"])
)
class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsCandidateUser()]
        if self.action == 'set_status':
            return [IsAuthenticated(), IsRecruiterUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Application.objects.none()

        user = self.request.user

        if user.role == "CANDIDATE":
            return Application.objects.filter(candidate=user)

        if user.role == "RECRUITER":
            return Application.objects.filter(
                job_offer__company__owner=user
            )

        return Application.objects.none()

    @extend_schema(
        summary="Changer le statut", 
        description="Réservé au recruteur pour accepter, refuser ou avancer une candidature.", 
        tags=["Candidatures"],
        responses={
            200: OpenApiResponse(description="Statut mis à jour avec succès."),
            400: OpenApiResponse(description="Requête mal formée (Statut invalide)."),
            403: OpenApiResponse(description="Refusé (Ce n'est pas votre offre ou vous êtes candidat)."),
            404: OpenApiResponse(description="Candidature introuvable.")
        }
    )
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