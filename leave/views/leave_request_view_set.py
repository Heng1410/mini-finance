from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response

from base.views.company_base_view_set import CompanyBaseViewSet
from leave.models.leave_request import LeaveRequest
from leave.serializers.leave_request_serializer import (
    LeaveRequestDetailSerializer,
    LeaveRequestListSerializer,
    LeaveRequestSerializer,
)
from leave.services.leave_request_service import LeaveRequestService


class LeaveRequestViewSet(CompanyBaseViewSet):
    model = LeaveRequest
    queryset = LeaveRequest.objects.select_related(
        "employee",
        "leave_type",
    )
    serializer_class = LeaveRequestSerializer
    filter_backends = CompanyBaseViewSet.filter_backends + (DjangoFilterBackend,)

    filterset_fields = {
        "status": ["exact"],
        "employee": ["exact"],
        "leave_type": ["exact"],
        "start_date": ["exact", "gte", "lte"],
        "end_date": ["exact", "gte", "lte"],
    }

    search_fields = [
        "employee__name",
        "leave_type__name",
        "status",
    ]

    def get_serializer_class(self):
        if self.action == "list":
            return LeaveRequestListSerializer

        if self.action == "retrieve":
            return LeaveRequestDetailSerializer

        return LeaveRequestSerializer

    def perform_create(self, serializer):
        serializer.save(
            company=self.get_company(),
            employee=self.request.user.employee,
        )

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        leave_request = LeaveRequestService.approve(
            company=self.get_company(), leave_request_id=pk
        )

        serializer = LeaveRequestDetailSerializer(
            leave_request, context=self.get_serializer_context()
        )

        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        leave_request = LeaveRequestService.reject(
            leave_request_id=pk,
            company=self.get_company(),
        )

        serializer = LeaveRequestDetailSerializer(
            leave_request, context=self.get_serializer_context()
        )

        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        leave_request = LeaveRequestService.cancel(
            leave_request_id=pk, company=self.get_company()
        )

        serializer = LeaveRequestDetailSerializer(
            leave_request,
            context=self.get_serializer_context(),
        )

        return Response(serializer.data)
