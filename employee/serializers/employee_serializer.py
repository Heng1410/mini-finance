from rest_framework import serializers

from base.serializers.base_serializer import BaseSerializer
from company.models.company import Company
from company.serializers.company_serializer import CompanyListSerializer
from department.models.department import Department
from department.serializers.department_serializer import DepartmentListSerializer
from employee.models.employee import Employee
from role.models.role import Role
from role.serializers.role_serializer import RoleListSerializer


class EmployeeSerializer(BaseSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())
    manager = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Employee
        fields = (
            "id",
            "company",
            "department",
            "manager",
            "role",
            "employee_code",
            "first_name",
            "last_name",
            "email",
            "phone",
            "hire_date",
            "job_title",
            "is_active",
        )


class EmployeeSimpleSerializer(BaseSerializer):
    class Meta:
        model = Employee
        fields = (
            "id",
            "employee_code",
            "first_name",
            "last_name",
        )


class EmployeeListSerializer(BaseSerializer):
    company = CompanyListSerializer(read_only=True)
    department = DepartmentListSerializer(read_only=True)
    role = RoleListSerializer(read_only=True)
    manager = EmployeeSimpleSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = (
            "id",
            "employee_code",
            "company",
            "department",
            "role",
            "manager",
            "first_name",
            "last_name",
            "email",
            "phone",
            "job_title",
            "is_active",
        )


class EmployeeDetailSerializer(EmployeeSerializer):
    company = CompanyListSerializer(read_only=True)
    department = DepartmentListSerializer(read_only=True)
    role = RoleListSerializer(read_only=True)
    manager = EmployeeSimpleSerializer(read_only=True)
    pass
