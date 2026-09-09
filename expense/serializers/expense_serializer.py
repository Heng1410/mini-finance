from rest_framework import serializers

from expense.models.expense import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = [
            "id",
            "employee",
            "date",
            "category",
            "description",
            "amount",
            "status",
            "reimbursed_at",
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


class ExpenseListSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()

    class Meta:
        model = Expense
        fields = [
            "id",
            "employee",
            "employee_name",
            "date",
            "category",
            "description",
            "amount",
            "status",
            "reimbursed_at",
        ]

    def get_employee_name(self, obj):
        return f"{obj.employee.first_name} {obj.employee.last_name}"


class ExpenseDetailSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()

    class Meta:
        model = Expense
        fields = [
            "id",
            "employee",
            "employee_name",
            "date",
            "category",
            "description",
            "amount",
            "status",
            "reimbursed_at",
            "created_at",
            "updated_at",
        ]

    def get_employee_name(self, obj):
        return f"{obj.employee.first_name} {obj.employee.last_name}"
