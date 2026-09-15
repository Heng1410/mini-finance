from rest_framework import serializers

from employee_document.models.employee_document import EmployeeDocument

class EmployeeDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeDocument
        fields = [
            "id",
            "employee",
            "name",
            "document_type",
            "file",
            "issued_date",
            "expiry_date",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "employee",
            "created_at",
            "updated_at",
        ]


class EmployeeDocumentListSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()

    class Meta:
        model = EmployeeDocument
        fields = [
            "id",
            "employee",
            "employee_name",
            "name",
            "document_type",
            "file",
            "issued_date",
            "expiry_date",
        ]

    def get_employee_name(self, obj):
        return f"{obj.employee.first_name} {obj.employee.last_name}"


class EmployeeDocumentDetailSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()

    class Meta:
        model = EmployeeDocument
        fields = [
            "id",
            "employee",
            "employee_name",
            "name",
            "document_type",
            "file",
            "issued_date",
            "expiry_date",
            "description",
            "created_at",
            "updated_at",
        ]

    def get_employee_name(self, obj):
        return f"{obj.employee.first_name} {obj.employee.last_name}"