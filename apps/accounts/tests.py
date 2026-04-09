from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from unittest.mock import patch

from apps.accounts.models import User, EmailOTP
from apps.accounts.services import create_user, create_otp, verify_otp
from apps.accounts.serializers import RegisterSerializer


class CreateUserServiceTest(TestCase):
    """
    Tests unitaires sur le service de création d'utilisateur.
    """

    def test_user_is_created_inactive(self):
        """Un utilisateur créé via create_user doit être inactif."""
        user = create_user("alice", "alice@test.com", "securepass123")
        self.assertFalse(user.is_active)

    def test_user_default_role_is_candidate(self):
        """Sans rôle explicite, le rôle par défaut doit être CANDIDATE."""
        user = create_user("bob", "bob@test.com", "securepass123")
        self.assertEqual(user.role, User.Role.CANDIDATE)

    def test_user_can_be_created_as_recruiter(self):
        """On peut explicitement créer un recruteur."""
        user = create_user("corp", "corp@test.com", "securepass123", role=User.Role.RECRUITER)
        self.assertEqual(user.role, User.Role.RECRUITER)


class CreateOTPServiceTest(TestCase):
    """
    Tests unitaires sur le service de génération d'OTP.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="otp_user",
            email="otp@test.com",
            password="pass",
            is_active=False
        )

    @patch("apps.accounts.services.send_mail")
    def test_otp_is_created(self, mock_mail):
        """Un OTP doit être créé en base pour l'utilisateur."""
        otp = create_otp(self.user)
        self.assertIsNotNone(otp)
        self.assertEqual(otp.user, self.user)
        self.assertFalse(otp.is_used)

    @patch("apps.accounts.services.send_mail")
    def test_otp_code_has_six_digits(self, mock_mail):
        """Le code OTP doit faire exactement 6 chiffres."""
        otp = create_otp(self.user)
        self.assertEqual(len(otp.code), 6)
        self.assertTrue(otp.code.isdigit())

    @patch("apps.accounts.services.send_mail")
    def test_email_is_sent(self, mock_mail):
        """L'email doit être expédié lors de la création de l'OTP."""
        create_otp(self.user)
        mock_mail.assert_called_once()

    @patch("apps.accounts.services.send_mail")
    def test_rate_limit_blocks_after_3_otps(self, mock_mail):
        """Le Rate Limiting doit bloquer après 3 OTPs en moins de 5 minutes."""
        for _ in range(3):
            EmailOTP.objects.create(user=self.user, code="123456")

        with self.assertRaises(ValueError):
            create_otp(self.user)


class VerifyOTPServiceTest(TestCase):
    """
    Tests unitaires sur le service de vérification d'OTP.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="verify_user",
            email="verify@test.com",
            password="pass",
            is_active=False
        )
        self.otp = EmailOTP.objects.create(user=self.user, code="999888")

    def test_valid_otp_activates_user(self):
        """Un OTP valide doit activer le compte de l'utilisateur."""
        result = verify_otp("verify@test.com", "999888")
        self.assertIsNotNone(result)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_invalid_code_returns_none(self):
        """Un mauvais code doit retourner None."""
        result = verify_otp("verify@test.com", "000000")
        self.assertIsNone(result)

    def test_expired_otp_returns_none(self):
        """Un OTP de plus de 5 minutes doit être rejeté."""
        self.otp.created_at = timezone.now() - timedelta(minutes=10)
        self.otp.save()
        result = verify_otp("verify@test.com", "999888")
        self.assertIsNone(result)

    def test_used_otp_returns_none(self):
        """Un OTP déjà utilisé doit être rejeté."""
        self.otp.is_used = True
        self.otp.save()
        result = verify_otp("verify@test.com", "999888")
        self.assertIsNone(result)

    def test_otp_marked_as_used_after_verification(self):
        """Après vérification, l'OTP doit être marqué comme utilisé."""
        verify_otp("verify@test.com", "999888")
        self.otp.refresh_from_db()
        self.assertTrue(self.otp.is_used)


class RegisterSerializerSecurityTest(TestCase):
    """
    Tests de sécurité sur le serializer d'inscription (Anti Mass Assignment).
    """

    def test_cannot_register_as_admin(self):
        """Un utilisateur ne doit pas pouvoir s'inscrire avec le rôle ADMIN."""
        data = {
            "username": "hacker",
            "email": "hacker@test.com",
            "password": "securepass123",
            "role": "ADMIN"
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("role", serializer.errors)

    def test_can_register_as_candidate(self):
        """L'inscription en tant que CANDIDATE doit être autorisée."""
        data = {
            "username": "candidate",
            "email": "candidate@test.com",
            "password": "securepass123",
            "role": "CANDIDATE"
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_can_register_as_recruiter(self):
        """L'inscription en tant que RECRUITER doit être autorisée."""
        data = {
            "username": "recruiter",
            "email": "recruiter@test.com",
            "password": "securepass123",
            "role": "RECRUITER"
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
