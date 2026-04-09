from django.test import TestCase

from apps.accounts.models import User
from apps.companies.models import Company
from apps.jobs.models import JobOffer, JobView
from apps.applications.models import Application
from apps.analytics.services import recruiter_stats, candidate_stats


def make_recruiter():
    return User.objects.create_user(
        username="recruiter", email="recruiter@test.com",
        password="pass", role=User.Role.RECRUITER, is_active=True
    )

def make_candidate(username="cand", email="cand@test.com"):
    return User.objects.create_user(
        username=username, email=email,
        password="pass", role=User.Role.CANDIDATE, is_active=True
    )


class RecruiterStatsServiceTest(TestCase):
    """
    Tests unitaires sur le dashboard Analytics recruteur.
    """

    def setUp(self):
        self.recruiter = make_recruiter()
        self.company = Company.objects.create(name="Acme", owner=self.recruiter)
        self.job = JobOffer.objects.create(
            title="Dev", description="desc", company=self.company,
            location="Paris", job_type="FULL_TIME"
        )
        self.candidate = make_candidate()

    def test_empty_stats(self):
        """Sans candidatures ni vues, tous les compteurs doivent être à zéro."""
        stats = recruiter_stats(self.recruiter)
        self.assertEqual(stats["total_jobs"], 1)
        self.assertEqual(stats["total_applications"], 0)
        self.assertEqual(stats["total_views"], 0)
        self.assertEqual(stats["conversion_rate"], 0)
        self.assertIsNone(stats["best_job"])

    def test_total_applications_counts_correctly(self):
        """Le total des candidatures doit refléter la BDD."""
        Application.objects.create(candidate=self.candidate, job_offer=self.job)
        stats = recruiter_stats(self.recruiter)
        self.assertEqual(stats["total_applications"], 1)

    def test_conversion_rate_calculation(self):
        """Le taux de conversion doit être calculé correctement."""
        # 1 vue et 1 candidature = 100%
        JobView.objects.create(job=self.job, user=self.candidate)
        Application.objects.create(candidate=self.candidate, job_offer=self.job)
        stats = recruiter_stats(self.recruiter)
        self.assertEqual(stats["conversion_rate"], 100.0)

    def test_conversion_rate_with_no_views_is_zero(self):
        """Sans vue, le taux de conversion doit être 0 (pas de division par zéro)."""
        Application.objects.create(candidate=self.candidate, job_offer=self.job)
        stats = recruiter_stats(self.recruiter)
        self.assertEqual(stats["conversion_rate"], 0)

    def test_best_job_is_identified(self):
        """Le job avec le plus de candidatures doit être identifié."""
        Application.objects.create(candidate=self.candidate, job_offer=self.job)
        stats = recruiter_stats(self.recruiter)
        self.assertEqual(stats["best_job"], "Dev")

    def test_status_counts_are_correct(self):
        """Les compteurs par statut doivent être exacts."""
        app = Application.objects.create(candidate=self.candidate, job_offer=self.job)
        app.status = "ACCEPTED"
        app.save()
        stats = recruiter_stats(self.recruiter)
        self.assertEqual(stats["accepted"], 1)
        self.assertEqual(stats["rejected"], 0)


class CandidateStatsServiceTest(TestCase):
    """
    Tests unitaires sur le dashboard Analytics candidat.
    """

    def setUp(self):
        self.recruiter = make_recruiter()
        self.company = Company.objects.create(name="Corp", owner=self.recruiter)
        self.job = JobOffer.objects.create(
            title="Dev", description="desc", company=self.company,
            location="Lyon", job_type="FULL_TIME"
        )
        self.candidate = make_candidate()

    def test_empty_stats(self):
        """Sans candidature, tous les compteurs doivent être à zéro."""
        stats = candidate_stats(self.candidate)
        self.assertEqual(stats["total_applications"], 0)
        self.assertEqual(stats["accepted"], 0)
        self.assertEqual(stats["rejected"], 0)
        self.assertEqual(stats["in_progress"], 0)

    def test_in_progress_count(self):
        """Les candidatures ni acceptées ni rejetées doivent être 'in_progress'."""
        Application.objects.create(
            candidate=self.candidate, job_offer=self.job, status="APPLIED"
        )
        stats = candidate_stats(self.candidate)
        self.assertEqual(stats["in_progress"], 1)
        self.assertEqual(stats["total_applications"], 1)

    def test_accepted_count(self):
        """Une candidature ACCEPTED doit incrémenter le bon compteur."""
        Application.objects.create(
            candidate=self.candidate, job_offer=self.job, status="ACCEPTED"
        )
        stats = candidate_stats(self.candidate)
        self.assertEqual(stats["accepted"], 1)
        self.assertEqual(stats["in_progress"], 0)

    def test_stats_are_scoped_to_candidate(self):
        """Les stats d'un candidat ne doivent pas inclure celles d'un autre."""
        other = make_candidate("other", "other@test.com")
        Application.objects.create(candidate=other, job_offer=self.job)
        stats = candidate_stats(self.candidate)
        self.assertEqual(stats["total_applications"], 0)
