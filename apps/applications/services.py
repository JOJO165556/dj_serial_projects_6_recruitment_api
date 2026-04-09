from .models import Application
from apps.jobs.models import JobOffer
from rest_framework.exceptions import ValidationError
from apps.notifications.services import create_notification

import logging

logger = logging.getLogger(__name__)

def create_application(user, job_id, **validated_data):
    """
    Service Métier : Soumission d'une candidature.
    1. Vérifie si l'utilisateur a le bon rôle.
    2. Valide l'existence et l'activation de l'Offre.
    3. Prévient les envois multiples (doublon).
    4. Envoie une notification bilatérale (Candidat et Recruteur).
    """

    #Vérifier rôle
    if user.role != "CANDIDATE":
        logger.warning(f"Unauthorized application attempt by {user.email}")
        raise ValidationError({"user": "Only candidates can apply"})

    #Vérifier job
    job = JobOffer.objects.filter(id=job_id, is_active=True).first()
    if not job:
        logger.error(f"Invalid job_id={job_id} by {user.email}")
        raise ValidationError({"job": "Invalid or inactive job"})

    #Empêcher double candidature
    if Application.objects.filter(candidate=user, job_offer=job).exists():
        logger.info(f"Duplicate application by {user.email} for job {job.title}")
        raise ValidationError({"application": "Already applied to this job"})

    #Notification candidat
    create_notification(
        user=user,
        title="Application submitted",
        message=f"You applied to {job.title}"
    )

    # Notification recruteur
    create_notification(
        user=job.company.owner,
        title="New application",
        message=f"{user.email} applied to {job.title}"
    )

    application = Application.objects.create(
        candidate=user,
        job_offer=job,
        **validated_data,
    )
    logger.info(f"Application created by {user.email} for job {job.title}")
    return application

def update_application_status(user, application_id, status):
    """
    Service Métier : Mise à jour du flux de recrutement.
    S'assure que seul le propriétaire (Recruteur) de l'entreprise ayant
    posté l'offre peut modifier le statut de la candidature.
    Déclenche une notification d'update au profil candidat.
    """

    application = Application.objects.filter(id=application_id).first()

    if not application:
        raise ValidationError({"application": "Not found"})

    #Vérifie ownership du job
    if application.job_offer.company.owner != user:
        raise ValidationError({"permission": "Not allowed"})

    application.status = status
    application.save()

    create_notification(
        user=application.candidate,
        title="Application update",
        message=f"Your application is now {status}"
    )

    return application