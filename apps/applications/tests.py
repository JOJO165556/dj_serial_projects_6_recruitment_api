from django.test import TestCase
from rest_framework.exceptions import ValidationError

from apps.accounts.models import User
from apps.companies.models import Company
from apps.jobs.models import JobOffer
from apps.applications.models import Application
from apps.applications.services import create_application, update_application_status


def make_recruiter(username="recruiter", email="recruiter@test.com"):
    return User.objects.create_user(
        username=username, email=email, password="pass",
        role=User.Role.RECRUITER, is_active=True
    )

def make_candidate(username="candidate", email="candidate@test.com"):
    return User.objects.create_user(
        username=username, email=email, password="pass",
        role=User.Role.CANDIDATE, is_active=True
    )

def make_company(owner):
    return Company.objects.create(name="Acme Corp", owner=owner)

def make_job(company, is_active=True):
    return JobOffer.objects.create(
        title="Dev Django",
        description="Senior dev",
        company=company,
        location="Paris",
        job_type="FULL_TIME",
        is_active=is_active
    )


class CreateApplicationServiceTest(TestCase):
    """
    Tests unitaires sur le service de création de candidature.
    """

    def setUp(self):
        self.recruiter = make_recruiter()
        self.candidate = make_candidate()
        self.company = make_company(self.recruiter)
        self.job = make_job(self.company)

    def test_valid_application_is_created(self):
        """Un candidat peut postuler à une offre active."""
        app = create_application(self.candidate, self.job.id)
        self.assertEqual(app.candidate, self.candidate)
        self.assertEqual(app.job_offer, self.job)
        self.assertEqual(app.status, Application.Status.APPLIED)

    def test_recruiter_cannot_apply(self):
        """Un recruteur ne doit pas pouvoir postuler."""
        with self.assertRaises(ValidationError) as ctx:
            create_application(self.recruiter, self.job.id)
        self.assertIn("user", ctx.exception.detail)

    def test_inactive_job_is_rejected(self):
        """Une candidature sur une offre inactive doit être rejetée."""
        inactive_job = make_job(self.company, is_active=False)
        with self.assertRaises(ValidationError) as ctx:
            create_application(self.candidate, inactive_job.id)
        self.assertIn("job", ctx.exception.detail)

    def test_nonexistent_job_is_rejected(self):
        """Un job_id inexistant doit être rejeté."""
        with self.assertRaises(ValidationError) as ctx:
            create_application(self.candidate, job_id=99999)
        self.assertIn("job", ctx.exception.detail)

    def test_duplicate_application_is_rejected(self):
        """Un candidat ne peut pas postuler deux fois à la même offre."""
        create_application(self.candidate, self.job.id)
        with self.assertRaises(ValidationError) as ctx:
            create_application(self.candidate, self.job.id)
        self.assertIn("application", ctx.exception.detail)

    def test_application_creates_notifications(self):
        """La candidature doit générer des notifications pour le candidat et le recruteur."""
        from apps.notifications.models import Notification
        create_application(self.candidate, self.job.id)
        self.assertEqual(Notification.objects.filter(user=self.candidate).count(), 1)
        self.assertEqual(Notification.objects.filter(user=self.recruiter).count(), 1)


class UpdateApplicationStatusServiceTest(TestCase):
    """
    Tests unitaires sur le service de mise à jour du statut.
    """

    def setUp(self):
        self.recruiter = make_recruiter()
        self.candidate = make_candidate()
        self.company = make_company(self.recruiter)
        self.job = make_job(self.company)
        self.application = create_application(self.candidate, self.job.id)

    def test_recruiter_can_update_status(self):
        """Le recruteur propriétaire peut changer le statut."""
        updated = update_application_status(self.recruiter, self.application.id, "INTERVIEW")
        self.assertEqual(updated.status, "INTERVIEW")

    def test_wrong_recruiter_cannot_update(self):
        """Un recruteur tiers ne peut pas modifier le statut d'une candidature."""
        other_recruiter = make_recruiter("other", "other@test.com")
        with self.assertRaises(ValidationError) as ctx:
            update_application_status(other_recruiter, self.application.id, "ACCEPTED")
        self.assertIn("permission", ctx.exception.detail)

    def test_nonexistent_application_raises(self):
        """Un ID de candidature inexistant doit lever une ValidationError."""
        with self.assertRaises(ValidationError) as ctx:
            update_application_status(self.recruiter, 99999, "ACCEPTED")
        self.assertIn("application", ctx.exception.detail)
