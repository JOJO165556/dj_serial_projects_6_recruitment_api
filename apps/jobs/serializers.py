from rest_framework import serializers
from .models import JobOffer

# Job Offer
class JobOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOffer
        fields = "__all__"
        read_only_fields = ["company"]

    def create(self, validated_data):
        from .services import create_job_offer
        owner = self.context["request"].user
        return create_job_offer(owner=owner, **validated_data)