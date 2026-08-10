from base.views.base_view_set import BaseViewSet
from department.models.department import Department
from department.serializers.department_serializer import (
    DepartmentDetailSerializer,
    DepartmentListSerializer,
    DepartmentSerializer,
)


class DepartmentViewSet(BaseViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = []

    def get_queryset(self):
        queryset = self.queryset.select_related("company")

        if self.action == "list":
            queryset = queryset.filter(is_active=True)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return DepartmentListSerializer

        if self.action == "retrieve":
            return DepartmentDetailSerializer

        return DepartmentSerializer
