from rest_framework import serializers

from base.serializers.base_serializer import BaseSerializer
from employee.serializers.employee_serializer import EmployeeSimpleSerializer
from leave.models.leave_request import LeaveRequest
from leave.serializers.leave_type_serializer import LeaveTypeListSerializer


class LeaveRequestSerializer(BaseSerializer):
    class Meta:
        model = LeaveRequest
        fields = [
            "id",
            "employee",
            "leave_type",
            "start_date",
            "end_date",
            "reason",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "employee",
            "status",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")

        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError(
                {
                    "end_date": (
                        "End date must be greater than or equal to " "start date."
                    )
                }
            )

        company = self.context["request"].user.employee.company

        employee = attrs.get("employee")
        leave_type = attrs.get("leave_type")

        if employee and employee.company_id != company.id:
            raise serializers.ValidationError(
                {"employee": ("Employee must belong to the current company.")}
            )

        if leave_type and leave_type.company_id != company.id:
            raise serializers.ValidationError(
                {"leave_type": ("Leave type must belong to the current company.")}
            )

        return attrs


class LeaveRequestListSerializer(serializers.ModelSerializer):
    employee = EmployeeSimpleSerializer(read_only=True)
    leave_type = LeaveTypeListSerializer(read_only=True)

    class Meta:
        model = LeaveRequest
        fields = [
            "id",
            "employee",
            "leave_type",
            "start_date",
            "end_date",
            "status",
        ]


class LeaveRequestDetailSerializer(serializers.ModelSerializer):
    employee = EmployeeSimpleSerializer(read_only=True)
    leave_type = LeaveTypeListSerializer(read_only=True)

    class Meta:
        model = LeaveRequest
        fields = [
            "id",
            "employee",
            "leave_type",
            "start_date",
            "end_date",
            "reason",
            "status",
            "created_at",
            "updated_at",
        ]
