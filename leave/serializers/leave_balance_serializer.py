from rest_framework import serializers

from base.serializers.base_serializer import BaseSerializer
from leave.models.leave_balance import LeaveBalance


class LeaveBalanceSerializer(BaseSerializer):
    remaining_days = serializers.SerializerMethodField()

    class Meta:
        model = LeaveBalance
        fields = [
            "id",
            "employee",
            "leave_type",
            "year",
            "allocated_days",
            "used_days",
            "remaining_days",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "employee",
            "used_days",
            "remaining_days",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        company = self.context["request"].user.employee.company

        employee = attrs.get("employee")
        leave_type = attrs.get("leave_type")

        if employee and employee.company_id != company.id:
            raise serializers.ValidationError(
                {"employee": "Employee must belong to the current company."}
            )

        if leave_type and leave_type.company_id != company.id:
            raise serializers.ValidationError(
                {"leave_type": "Leave type must belong to the current company."}
            )

        return attrs

    def get_remaining_days(self, obj):
        return obj.allocated_days - obj.used_days


class LeaveBalanceListSerializer(BaseSerializer):
    employee_name = serializers.CharField(
        source="employee.name",
        read_only=True,
    )
    leave_type_name = serializers.CharField(
        source="leave_type.name",
        read_only=True,
    )
    remaining_days = serializers.SerializerMethodField()

    class Meta:
        model = LeaveBalance
        fields = [
            "id",
            "employee",
            "employee_name",
            "leave_type",
            "leave_type_name",
            "year",
            "allocated_days",
            "used_days",
            "remaining_days",
        ]

    def get_remaining_days(self, obj):
        return obj.allocated_days - obj.used_days


class LeaveBalanceDetailSerializer(BaseSerializer):
    employee_name = serializers.CharField(
        source="employee.name",
        read_only=True,
    )
    leave_type_name = serializers.CharField(
        source="leave_type.name",
        read_only=True,
    )
    remaining_days = serializers.SerializerMethodField()

    class Meta:
        model = LeaveBalance
        fields = [
            "id",
            "employee",
            "employee_name",
            "leave_type",
            "leave_type_name",
            "year",
            "allocated_days",
            "used_days",
            "remaining_days",
            "created_at",
            "updated_at",
        ]

    def get_remaining_days(self, obj):
        return obj.allocated_days - obj.used_days
