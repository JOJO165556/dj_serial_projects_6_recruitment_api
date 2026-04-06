import random

from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        RECRUITER = "RECRUITER", "Recruiter"
        CANDIDATE = "CANDIDATE", "Candidate"

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CANDIDATE) #type: ignore

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

class EmailOTP(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def generate_otp(self):
        return str(random.randint(100000, 999999))

    @staticmethod
    def send_otp(email, code):
        send_mail(
            "Your OTP Code",
            f"Your verification code is {code}",
            "no-reply@system.com",
            [email],
        )