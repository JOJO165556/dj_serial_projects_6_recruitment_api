from .models import JobOffer, JobView
from apps.companies.models import Company
from rest_framework.exceptions import ValidationError

def create_job_offer(owner, company_id, **validated_data):
    """
    Crée une offre d'emploi pour une entreprise dont l'utilisateur est propriétaire.
    """
    company = Company.objects.filter(id=company_id,owner=owner).first()

    if not company:
        raise ValidationError("Invalid company")

    return JobOffer.objects.create(company=company, **validated_data)

def track_job_view(job, user=None):
    """
    Enregistre une vue sur une offre.
    """

    JobView.objects.create(
        job=job,
        user=user if user and user.is_authenticated else None
    )
