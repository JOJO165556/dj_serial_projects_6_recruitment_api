from .models import JobOffer
from companies.models import Company
from rest_framework.exceptions import ValidationError

def create_job_offer(owner, **validated_data):
    """
    Crée une nouvelle offre d'emploi pour la première entreprise dont l'utilisateur est propriétaire.
    """
    company = Company.objects.filter(owner=owner).first()
    if not company:
        raise ValidationError({"company": "You must create a company first."})
    return JobOffer.objects.create(company=company, **validated_data)
