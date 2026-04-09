from rest_framework import serializers
from .models import Application
from .services import create_application
from .validators import validate_file


class ApplicationSerializer(serializers.ModelSerializer):
    job_id = serializers.IntegerField(write_only=True)
    cover_letter = serializers.FileField(validators=[validate_file])

    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = ["candidate", "status"]

    def create(self, validated_data):
        """
        Délègue la création au service.
        """
        user = self.context["request"].user
        job_id = validated_data.pop("job_id")

        return create_application(
            user=user,
            job_id=job_id,
            **validated_data
        )