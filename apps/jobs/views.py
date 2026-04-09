from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .filters import JobOfferFilter
from .models import JobOffer
from .serializers import JobOfferSerializer
from apps.accounts.permissions import IsRecruiterUser
from rest_framework.permissions import IsAuthenticated, AllowAny

from .services import track_job_view


# Job Offer
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

class PublicJobOfferViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Liste publique des jobs pour candidats.
    """

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