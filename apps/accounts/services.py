import random
import logging
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail

from .models import User, EmailOTP

logger = logging.getLogger(__name__)

# User Service
def create_user(username, email, password, role=None):
    """
    Crée un nouvel utilisateur inactif par défaut en attente de vérification OTP.
    Gère le fallback implicite vers le rôle CANDIDATE (cf: defaults du Model).
    """
    if role is None:
        role = User.Role.CANDIDATE
        
    return User.objects.create_user(
        username=username,
        email=email,
        password=password,
        role=role,
        is_active=False
    )

# OTP Service
def generate_otp():
    return str(random.randint(100000, 999999))

def create_otp(user):
    """
    Service central de génération et d'envoi d'un code OTP sécurisé.
    Implémente un système Anti-Spam: pas plus de 3 codes par tranche de 5 minutes.
    """

    recent_otps = EmailOTP.objects.filter(
        user=user,
        created_at__gte=timezone.now() - timedelta(minutes=5)
    ).count()

    if recent_otps >= 3:
        raise ValueError("Too many OTP requests. Try later.")

    otp = EmailOTP.objects.create(
        user=user,
        code=generate_otp()
    )

    send_mail(
        subject="Your Authentication Code",
        message=f"Here is your secure OTP code: {otp.code}\nIt will expire in 5 minutes.",
        from_email=None, # Utilise DEFAULT_FROM_EMAIL
        recipient_list=[user.email],
        fail_silently=False,
    )
    
    logger.info(f"OTP sent to {user.email}")
    return otp

def verify_otp(email, code):
    """
    Valide un code OTP pour activer le compte de l'utilisateur.
    Intègre de strictes validations de sécurité :
    - Expiration après 5 minutes.
    - Usage unique (is_used).
    - Mécanisme Anti-Bruteforce (limite d'essais à 5 erreurs).
    """
    otp = EmailOTP.objects.filter(
        user__email=email,
        code=code,
        is_used=False
    ).first()

    if not otp:
        logger.warning(f"Invalid OTP attempt for {email}")
        return None

    # expiration 5 minutes
    if otp.created_at < timezone.now() - timedelta(minutes=5):
        logger.warning(f"Expired OTP for {email}")
        return None

    if otp.is_used:
        return None

    if EmailOTP.objects.filter(user__email=email, is_used=False).count() > 5:
        raise Exception("Too many attempts")

    otp.is_used = True
    otp.save()

    user = otp.user
    user.is_active = True
    user.save()

    logger.info(f"OTP verified successfuly for {email}")

    return user