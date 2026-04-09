from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .filters import JobOfferFilter
from .models import JobOffer
from .serializers import JobOfferSerializer
from apps.accounts.permissions import IsRecruiterUser
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema_view, extend_schema

from .services import track_job_view


@extend_schema_view(
    list=extend_schema(summary="Lister mes offres", description="Renvoie uniquement les offres des entreprises que le recruteur gère.", tags=["Offres (Recruteur)"]),
    create=extend_schema(summary="Créer une offre", tags=["Offres (Recruteur)"]),
    retrieve=extend_schema(summary="Détail d'une offre recruteur", tags=["Offres (Recruteur)"]),
    update=extend_schema(summary="Mettre à jour complètement", tags=["Offres (Recruteur)"]),
    partial_update=extend_schema(summary="Mettre à jour partiellement", tags=["Offres (Recruteur)"]),
    destroy=extend_schema(summary="Supprimer l'offre", tags=["Offres (Recruteur)"])
)
class JobOfferViewSet(viewsets.ModelViewSet):
    queryset = JobOffer.objects.all()
    serializer_class = JobOfferSerializer
    permission_classes = [IsAuthenticated, IsRecruiterUser]

    #Activation de filtering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = JobOfferFilter

    #Recherche texte
    search_fields = ["title", "description", "location"]

    def get_queryset(self):
        return JobOffer.objects.filter(company__owner=self.request.user)

@extend_schema_view(
    list=extend_schema(summary="Portail des offres actives", description="Catalogue de toutes les offres actuellement accessibles au grand public.", tags=["Offres (Public)"]),
    retrieve=extend_schema(summary="Consulter une offre", description="Renvoie les détails et incrémente le compteur de vues.", tags=["Offres (Public)"])
)
class PublicJobOfferViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = JobOfferSerializer
    permission_classes = [AllowAny]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = JobOfferFilter
    search_fields = ["title", "description", "location"]

    def get_queryset(self):
        return JobOffer.objects.filter(is_active=True)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        track_job_view(instance, request.user)

        return super().retrieve(request, *args, **kwargs)