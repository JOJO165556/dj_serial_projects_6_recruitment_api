from rest_framework import serializers
from .models import JobOffer
from .services import create_job_offer

# Job Offer
class JobOfferSerializer(serializers.ModelSerializer):
    company_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = JobOffer
        fields = "__all__"
        read_only_fields = ["company"]

    def create(self, validated_data):
        """
        Délègue la création au service en injectant owner et company_id
        """
        owner = self.context["request"].user
        company_id = validated_data.pop("company_id")

        return create_job_offer(
            owner=owner,
            company_id=company_id,
            **validated_data
        )