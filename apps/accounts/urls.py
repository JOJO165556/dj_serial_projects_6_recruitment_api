from django.urls import path
from .views import RegisterView, MeView, EmailLoginView, LogoutView, VerifyOTPView, CustomTokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('verify-otp/', VerifyOTPView.as_view()),
    path('me/', MeView.as_view()),
    path('login/', EmailLoginView.as_view()),
    path('refresh/', CustomTokenRefreshView.as_view()),
    path('logout/', LogoutView.as_view()),
]