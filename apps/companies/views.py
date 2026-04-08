from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.accounts.permissions import IsRecruiterUser
from .models import Company
from .serializers import CompanySerializer

# Company
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsRecruiterUser]

    def get_queryset(self):
        return Company.objects.filter(owner=self.request.user)
