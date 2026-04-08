from rest_framework import serializers
from .models import CandidateProfile
from .services import create_candidate_profile

class CandidateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateProfile
        fields = "__all__"
        read_only_fields = ["user"]

    def create(self, **validated_data):
        """
        Délègue au service avec user connecté.
        """
        user = self.context["request"].user

        return create_candidate_profile(
            user=user,
            **validated_data
        )