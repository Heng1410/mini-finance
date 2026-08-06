from rest_framework import serializers

from base.serializers.base_serializer import BaseSerializer
from company.models.company import Company
from company.serializers.company_serializer import CompanyListSerializer
from department.models.department import Department


class DepartmentSerializer(BaseSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())

    class Meta:
        model = Department
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
        value = value.strip().upper()

        if not value:
            raise serializers.ValidationError("Department name cannot be empty.")

        return value

    def validate_code(self, value):
        value = value.strip().upper()

        if not value:
            raise serializers.ValidationError("Department code cannot be empty.")

        return value


class DepartmentListSerializer(BaseSerializer):
    company = CompanyListSerializer(read_only=True)

    class Meta:
        model = Department
        fields = (
            "id",
            "company",
            "name",
            "code",
            "description",
            "is_active",
        )


class DepartmentDetailSerializer(BaseSerializer):
    company = CompanyListSerializer(read_only=True)

    class Meta:
        model = Department
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
