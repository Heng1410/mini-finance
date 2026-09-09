from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from datetime import date

from attendance.models.attendance import Attendance
from attendance.serializers.attendance_report_serializer import (
    AttendanceSummaryQuerySerializer,
    AttendanceSummarySerializer,
)
from attendance.serializers.attendance_serializer import (
    AttendanceCheckInSerializer,
    AttendanceCheckOutSerializer,
    AttendanceDetailSerializer,
    AttendanceListSerializer,
    AttendanceSerializer,
)
from attendance.services.attendance_report_service import AttendanceReportService
from attendance.services.attendance_service import AttendanceService
from base.views.company_base_view_set import CompanyBaseViewSet


class AttendanceViewSet(CompanyBaseViewSet):
    model = Attendance
    queryset = Attendance.objects.select_related("employee")
    serializer_class = AttendanceSerializer

    filter_backends = CompanyBaseViewSet.filter_backends + (DjangoFilterBackend,)

    filterset_fields = {
        "employee": ["exact"],
        "date": ["exact", "gte", "lte"],
        "status": ["exact"],
    }

    search_fields = [
        "employee__first_name",
        "employee__last_name",
        "status",
        "note",
    ]

    def get_serializer_class(self):
        if self.action == "list":
            return AttendanceListSerializer

        if self.action == "retrieve":
            return AttendanceDetailSerializer

        return AttendanceSerializer

    def perform_create(self, serializer):
        serializer.save(
            company=self.get_company(),
            employee=self.request.user.employee,
        )

    @action(detail=False, methods=["post"])
    def check_in(self, request):
        serializer = AttendanceCheckInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        attendance = AttendanceService.check_in(
            employee=request.user.employee,
            date=serializer.validated_data["date"],
            check_in=serializer.validated_data["check_in"],
        )

        serializer = AttendanceDetailSerializer(attendance)

        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def check_out(self, request):
        serializer = AttendanceCheckOutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        attendance = AttendanceService.check_out(
            employee=request.user.employee,
            date=serializer.validated_data["date"],
            check_out=serializer.validated_data["check_out"],
        )

        serializer = AttendanceDetailSerializer(attendance)

        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def summary(self, request):
        query_serializer = AttendanceSummaryQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)

        employee = request.user.employee

        summary = AttendanceReportService.get_summary(
            employee=employee, **query_serializer.validated_data
        )

        serializer = AttendanceSummarySerializer(summary)

        return Response(serializer.data)
