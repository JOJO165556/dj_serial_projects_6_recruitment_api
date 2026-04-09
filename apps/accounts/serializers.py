from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User

# Register
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "role"]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_role(self, value):
        """
        Sécurité (Bloque l'assignation en masse) : 
        Empêche un utilisateur malveillant de s'inscrire en tant qu'ADMIN
        tout en autorisant le choix explicite du rôle RECRUITER ou CANDIDATE.
        """
        if value == User.Role.ADMIN:
            raise serializers.ValidationError("You cannot register an Admin account.")
        return value

    def create(self, validated_data):
        from .services import create_user
        return create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            role=validated_data.get("role")
        )

# User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "role"]
        read_only_fields = ["id", "email", "role"]

# Email Token Obtain Pair
class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"

    def validate(self, attrs):
        attrs["username"] = attrs.get("email")
        return super().validate(attrs)
