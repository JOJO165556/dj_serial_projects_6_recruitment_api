from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User, EmailOTP
from .serializers import RegisterSerializer, UserSerializer, EmailTokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class EmailLoginView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out"})
        except Exception:
            return Response({"error": "Invalid token"}, status=400)

class VerifyOTPView(APIView):
    def post(self, request):
        email = request.data['email']
        code = request.data['code']

        otp = EmailOTP.objects.filter(
            user__email=email,
            code=code,
            is_used=False
        ).first()

        if not otp:
            return Response({"error": "Invalid OTP"}, status=400)

        otp.is_used = True
        otp.save()

        user = otp.user
        user.is_active = True
        user.save()

        return Response({"message": "Email verified"})
