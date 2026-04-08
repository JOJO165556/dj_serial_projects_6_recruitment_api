from .models import Company

def create_company(owner, **validated_data):
    """
    Crée une nouvelle entreprise associée à un utilisateur (propriétaire).
    """
    return Company.objects.create(owner=owner, **validated_data)
