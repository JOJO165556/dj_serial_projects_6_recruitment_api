import random
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from django.utils import timezone

from .models import User, EmailOTP

# Auth Service
def login_user(email, password):
    user = authenticate(username=email, password=password)

    if not user:
        return None

    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

# User Service
def create_user(username, email, password, role=None):
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
    return EmailOTP.objects.create(
        user=user,
        code=generate_otp()
    )

def verify_otp(email, code):
    otp = EmailOTP.objects.filter(
        user__email=email,
        code=code,
        is_used=False
    ).first()

    if not otp:
        return None

    if otp.is_used:
        return None

    # expiration 5 minutes
    if otp.created_at < timezone.now() - timedelta(minutes=5):
        return None

    otp.is_used = True
    otp.save()

    user = otp.user
    user.is_active = True
    user.save()

    return user