from apps.jobs.models import JobOffer
from apps.applications.models import Application
from apps.jobs.models import JobView


def recruiter_stats(user):
    """
    Service Métier : Statistiques Recruteur (Dashboard).
    Agrège les performances globales des annonces d'un recruteur.
    Calcule automatiquement le Taux de Conversion, et identifie le poste le plus attractif
    via une boucle sur les relations inversées (applications.count).
    """
    jobs = JobOffer.objects.filter(company__owner=user)
    applications = Application.objects.filter(job_offer__in=jobs)
    views = JobView.objects.filter(job__in=jobs)

    total_jobs = jobs.count()
    total_applications = applications.count()
    total_views = views.count()

    #Evite division par 0
    conversion_rate = (
        (total_applications / total_views) * 100
        if total_views > 0 else 0
    )

    #Job le plus performant
    best_job = None
    best_count = 0

    for job in jobs:
        count = job.applications.count() # type: ignore
        if count > best_count:
            best_count = count
            best_job = job.title

    return {
        "total_jobs": total_jobs,
        "total_views": total_views,
        "total_applications": total_applications,
        "interview": applications.filter(status="INTERVIEW").count(),
        "accepted": applications.filter(status="ACCEPTED").count(),
        "rejected": applications.filter(status="REJECTED").count(),
        "conversion_rate": round(conversion_rate, 2),
        "best_job": best_job,
    }

def candidate_stats(user):
    """
    Service Métier : Dashboard Candidat.
    Affiche le suivi général de ses postulations (Statuts, Acceptations, Rejets, En cours).
    """

    applications = Application.objects.filter(candidate=user)

    return {
        "total_applications": applications.count(),
        "accepted": applications.filter(status="ACCEPTED").count(),
        "rejected": applications.filter(status="REJECTED").count(),
        "in_progress": applications.exclude(
            status__in=["ACCEPTED", "REJECTED"]
        ).count(),
    }