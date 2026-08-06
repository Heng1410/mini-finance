from rest_framework import serializers
from base.serializers.base_serializer import BaseSerializer
from company.models.company import Company
from company.serializers.company_serializer import CompanyListSerializer
from role.models.role import Role


class RoleSerializer(BaseSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())

    class Meta:
        model = Role
        fields = (
            "id",
            "company",
            "name",
            "code",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        )

    def validate_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Role name cannot be empty.")

        return value

    def validate_code(self, value):
        value = value.strip().upper()

        if not value:
            raise serializers.ValidationError("Role code cannot be empty.")

        return value


class RoleListSerializer(BaseSerializer):
    company = CompanyListSerializer(read_only=True)

    class Meta:
        model = Role
        fields = (
            "id",
            "company",
            "name",
            "code",
            "description",
            "is_active",
        )


class RoleDetailSerializer(RoleSerializer):
    company = CompanyListSerializer(read_only=True)
    pass
