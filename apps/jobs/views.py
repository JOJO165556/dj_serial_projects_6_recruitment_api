from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import JobOffer
from .serializers import JobOfferSerializer
from apps.accounts.permissions import IsRecruiterUser

# Job Offer
class JobOfferViewSet(viewsets.ModelViewSet):
    queryset = JobOffer.objects.all()
    serializer_class = JobOfferSerializer
    permission_classes = [IsAuthenticated, IsRecruiterUser]

    def get_queryset(self):
        return JobOffer.objects.filter(company__owner=self.request.user)