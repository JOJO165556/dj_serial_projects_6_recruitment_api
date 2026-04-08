from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

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

    def perform_create(self, serializer):
        user = serializer.save()
        create_otp(user)

# Me
class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

# Login (JWT)
class EmailLoginView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer

# Logout
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

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

    def post(self, request):
        user = verify_otp(
            request.data["email"],
            request.data["code"]
        )

        if not user:
            return Response({"error": "Invalid OTP"}, status=400)

        return Response({"message": "Email verified"})