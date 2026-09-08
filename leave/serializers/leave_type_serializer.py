from rest_framework import serializers

from leave.models.leave_type import LeaveType


class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = [
            "id",
            "code",
            "name",
            "description",
            "days_per_year",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_code(self, value):
        return value.strip().upper()

    def validate_name(self, value):
        return value.strip()


class LeaveTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = [
            "id",
            "code",
            "name",
            "days_per_year",
            "is_active",
        ]


class LeaveTypeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = [
            "id",
            "code",
            "name",
            "description",
            "days_per_year",
            "is_active",
            "created_at",
            "updated_at",
        ]