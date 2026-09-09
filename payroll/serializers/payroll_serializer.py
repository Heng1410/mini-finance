from rest_framework import serializers

from payroll.models.payroll import Payroll


class PayrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payroll
        fields = [
            "id",
            "employee",
            "year",
            "month",
            "basic_salary",
            "allowance",
            "deduction",
            "net_salary",
            "is_paid",
            "paid_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "employee",
            "net_salary",
            "is_paid",
            "paid_at",
            "created_at",
            "updated_at",
        ]


class PayrollListSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()

    class Meta:
        model = Payroll
        fields = [
            "id",
            "employee",
            "employee_name",
            "year",
            "month",
            "basic_salary",
            "allowance",
            "deduction",
            "net_salary",
            "is_paid",
            "paid_at",
        ]

    def get_employee_name(self, obj):
        return f"{obj.employee.first_name} {obj.employee.last_name}"


class PayrollDetailSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()

    class Meta:
        model = Payroll
        fields = [
            "id",
            "employee",
            "employee_name",
            "year",
            "month",
            "basic_salary",
            "allowance",
            "deduction",
            "net_salary",
            "is_paid",
            "paid_at",
            "created_at",
            "updated_at",
        ]

    def get_employee_name(self, obj):
        return f"{obj.employee.first_name} {obj.employee.last_name}"