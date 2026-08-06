from rest_framework import serializers

from base.serializers.base_serializer import BaseSerializer
from company.models.company import Company


class CompanySerializer(BaseSerializer):

    class Meta:
        model = Company
        fields = (
            "id",
            "name",
            "code",
            "legal_name",
            "registration_number",
            "tax_number",
            "email",
            "phone",
            "website",
            "address_line_1",
            "address_line_2",
            "city",
            "country",
            "currency",
            "timezone",
            "fiscal_year_start",
            "logo",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        )

    def validate_code(self, value):
        value = value.strip().upper()

        if not value:
            raise serializers.ValidationError("Company code cannot be empty.")

        return value

    def validate_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Company name cannot be empty.")

        return value


class CompanyListSerializer(BaseSerializer):
    class Meta:
        model = Company
        fields = (
            "id",
            "name",
            "code",
            "email",
            "is_active",
        )


class CompanyDetailSerializer(CompanySerializer):
    pass
