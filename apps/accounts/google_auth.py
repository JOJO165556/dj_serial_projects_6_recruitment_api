from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiResponse
from apps.accounts.models import User

import requests


class GoogleLoginView(APIView):
    """
    Authentification sociale via Google OAuth2.
    Accepte un Access Token Google (émis côté client/frontend),
    le vérifie auprès de l'API Google, puis retourne une paire
    de tokens JWT (Access + Refresh) propres à cette API.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Connexion via Google",
        description="Échangez un Access Token Google contre une paire de tokens JWT de l'API. Le token Google doit être obtenu côté client (frontend) via le flux OAuth2.",
        tags=["Authentification"],
        responses={
            200: OpenApiResponse(description="Connexion réussie. Retourne access et refresh JWT."),
            400: OpenApiResponse(description="Token Google manquant dans le corps de la requête."),
            401: OpenApiResponse(description="Token Google invalide ou expiré."),
        }
    )
    def post(self, request):
        token = request.data.get("access_token")

        if not token:
            return Response({"error": "access_token is required"}, status=400)

        # Vérification du token auprès de l'API Google
        google_url = "https://www.googleapis.com/oauth2/v3/userinfo"
        response = requests.get(google_url, headers={"Authorization": f"Bearer {token}"})

        if response.status_code != 200:
            return Response({"error": "Invalid Google token"}, status=401)

        google_data = response.json()
        email = google_data.get("email")
        name = google_data.get("name", email)

        if not email:
            return Response({"error": "Could not retrieve email from Google"}, status=401)

        # Création ou récupération du compte
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": email.split("@")[0],
                "is_active": True,  # Compte Google = email déjà vérifié
            }
        )

        # Génération de la paire de tokens JWT
        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "created": created,  # True si c'est la première connexion
        })
