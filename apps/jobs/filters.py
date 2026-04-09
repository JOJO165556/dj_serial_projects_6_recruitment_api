import django_filters
from .models import JobOffer

class JobOfferFilter(django_filters.FilterSet):
    """
    Filtres disponibles pour les offres d'emploi.
    """

    title = django_filters.CharFilter(lookup_expr='icontains')
    location = django_filters.CharFilter(lookup_expr='icontains')
    job_type = django_filters.CharFilter()

    salary_min = django_filters.NumberFilter(field_name='salary_min', lookup_expr='gte')
    salary_max = django_filters.NumberFilter(field_name='salary_max', lookup_expr='lte')

    class Meta:
        model = JobOffer
        fields = ["title", "location", "job_type"]
