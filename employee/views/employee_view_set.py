from base.views.base_view_set import BaseViewSet
from employee.models.employee import Employee
from employee.serializers.employee_serializer import (
    EmployeeDetailSerializer,
    EmployeeListSerializer,
    EmployeeSerializer,
)


class EmployeeViewSet(BaseViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        queryset = self.queryset.select_related("company", "department", "manager","role")
        return querysets

    def get_serializer_class(self):
        if self.action == "list":
            return EmployeeListSerializer

        if self.action == "retrieve":
            return EmployeeDetailSerializer

        return EmployeeSerializer
