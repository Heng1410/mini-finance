from django_filters.rest_framework import DjangoFilterBackend

from base.views.company_base_view_set import CompanyBaseViewSet
from leave.models.leave_balance import LeaveBalance
from leave.serializers.leave_balance_serializer import (
    LeaveBalanceDetailSerializer,
    LeaveBalanceListSerializer,
    LeaveBalanceSerializer,
)


class LeaveBalanceViewSet(CompanyBaseViewSet):
    model = LeaveBalance
    queryset = LeaveBalance.objects.select_related(
        "employee",
        "leave_type",
    )
    serializer_class = LeaveBalanceSerializer
    filter_backends = CompanyBaseViewSet.filter_backends + (DjangoFilterBackend,)

    filterset_fields = {
        "employee": ["exact"],
        "leave_type": ["exact"],
        "year": ["exact"],
    }

    search_fields = [
        "employee__name",
        "leave_type__name",
    ]

    def get_serializer_class(self):
        if self.action == "list":
            return LeaveBalanceListSerializer

        if self.action == "retrieve":
            return LeaveBalanceDetailSerializer

        return LeaveBalanceSerializer

    def perform_create(self, serializer):
        serializer.save(
            company=self.get_company(),
            employee=self.request.user.employee,
        )
