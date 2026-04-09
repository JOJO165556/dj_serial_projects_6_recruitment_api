from .models import Application
from apps.jobs.models import JobOffer
from rest_framework.exceptions import ValidationError
from apps.notifications.services import create_notification

def create_application(user, job_id, **validated_data):
    """
    Crée une candidature.
    """

    #Vérifier rôle
    if user.role != "CANDIDATE":
        raise ValidationError({"user": "Only candidates can apply"})

    #Vérifier job
    job = JobOffer.objects.filter(id=job_id, is_active=True).first()
    if not job:
        raise ValidationError({"job": "Invalid or inactive job"})

    #Empêcher double candidature
    if Application.objects.filter(candidate=user, job_offer=job).exists():
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

    return Application.objects.create(
        candidate=user,
        job_offer=job,
        **validated_data,
    )

def update_application_status(user, application_id, status):
    """
    Met à jour le statut d'une candidature.
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