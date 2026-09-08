from base.views.company_base_view_set import CompanyBaseViewSet

from leave.models.leave_type import LeaveType
from leave.serializers.leave_type_serializer import (
    LeaveTypeDetailSerializer,
    LeaveTypeListSerializer,
    LeaveTypeSerializer,
)


class LeaveTypeViewSet(CompanyBaseViewSet):
    model = LeaveType
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeSerializer

    search_fields = [
        "code",
        "name",
    ]

    def get_serializer_class(self):
        if self.action == "list":
            return LeaveTypeListSerializer

        if self.action == "retrieve":
            return LeaveTypeDetailSerializer

        return LeaveTypeSerializer