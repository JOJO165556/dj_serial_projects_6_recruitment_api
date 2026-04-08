from rest_framework import serializers
from .models import Company

# Company
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"
        read_only_fields = ["owner"]

    def create(self, validated_data):
        from .services import create_company
        owner = self.context["request"].user
        return create_company(owner=owner, **validated_data)