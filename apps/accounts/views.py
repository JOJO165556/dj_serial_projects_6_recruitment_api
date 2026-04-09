from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .models import User
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    EmailTokenObtainPairSerializer
)

from .services import (
    create_otp,
    verify_otp
)

# Register
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Créer un compte", 
        description="Permet de s'inscrire et déclenche l'envoi d'un OTP par email.", 
        tags=["Authentification"],
        responses={
            201: OpenApiResponse(description="Compte créé et OTP envoyé."),
            400: OpenApiResponse(description="Données invalides (email déjà existant, etc).")
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = serializer.save()
        create_otp(user)

# Me
class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Mon Profil", description="Renvoie les informations du profil connecté.", tags=["Authentification"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        return self.request.user

# Login (JWT)
class EmailLoginView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer

    @extend_schema(
        summary="Connexion JWT", 
        description="Authentification avec email et mot de passe.", 
        tags=["Authentification"],
        responses={
            200: OpenApiResponse(description="Connexion réussie (Access + Refresh tokens)."),
            401: OpenApiResponse(description="Identifiants incorrects ou compte inactif.")
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class CustomTokenRefreshView(TokenRefreshView):
    @extend_schema(
        summary="Rafraîchir le token JWT", 
        description="Renvoie un nouveau Access Token en échange d'un Refresh Token valide.", 
        tags=["Authentification"],
        responses={
            200: OpenApiResponse(description="Nouveau Access Token généré."),
            401: OpenApiResponse(description="Refresh Token invalide, expiré ou blacklisté.")
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

# Logout
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Déconnexion", description="Blackliste le token JWT.", tags=["Authentification"])
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Logged out"})
        except Exception:
            return Response({"error": "Invalid token"}, status=400)

# Verify OTP
class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Vérifier le code OTP", 
        description="Valide le code à 6 chiffres envoyé.", 
        tags=["Authentification"],
        responses={
            200: OpenApiResponse(description="Email vérifié et compte activé."),
            400: OpenApiResponse(description="Code invalide, expiré ou introuvable."),
            403: OpenApiResponse(description="Compte temporairement bloqué (Sur-sollicitation OTP).")
        }
    )
    def post(self, request):
        user = verify_otp(
            request.data["email"],
            request.data["code"]
        )

        if not user:
            return Response({"error": "Invalid OTP"}, status=400)

        return Response({"message": "Email verified"})