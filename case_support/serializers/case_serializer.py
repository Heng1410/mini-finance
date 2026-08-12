from accounts_receivable.serializers.customer_serializer import CustomerListSerializer
from base.serializers.base_serializer import BaseSerializer
from case_support.models.case import Case
from employee.serializers.employee_serializer import EmployeeSimpleSerializer


class CaseSerializer(BaseSerializer):
    class Meta:
        model = Case
        fields = (
            "id",
            "case_number",
            "title",
            "description",
            "status",
            "priority",
            "customer",
            "assigned_to",
            "resolution_note",
        )
        read_only_fields = ("id", "case_number", "status", "assigned_to")


class CaseListSerializer(BaseSerializer):
    customer = CustomerListSerializer(read_only=True)
    assigned_to = EmployeeSimpleSerializer(read_only=True)

    class Meta:
        model = Case
        fields = (
            "id",
            "case_number",
            "title",
            "status",
            "priority",
            "customer",
            "assigned_to",
        )


class CaseDetailSerializer(CaseSerializer):
    customer = CustomerListSerializer(read_only=True)
    assigned_to = EmployeeSimpleSerializer(read_only=True)
