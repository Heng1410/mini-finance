from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from base.views.company_base_view_set import CompanyBaseViewSet
from payroll.models.payroll import Payroll
from payroll.serializers.payroll_serializer import (
    PayrollDetailSerializer,
    PayrollListSerializer,
    PayrollSerializer,
)
from payroll.services.payroll_service import PayrollService


class PayrollViewSet(CompanyBaseViewSet):
    model = Payroll

    queryset = Payroll.objects.select_related("employee")

    serializer_class = PayrollSerializer

    filter_backends = CompanyBaseViewSet.filter_backends + (DjangoFilterBackend,)

    filterset_fields = {
        "employee": ["exact"],
        "year": ["exact"],
        "month": ["exact"],
        "is_paid": ["exact"],
    }

    search_fields = [
        "employee__first_name",
        "employee__last_name",
    ]

    def get_serializer_class(self):
        if self.action == "list":
            return PayrollListSerializer

        if self.action == "retrieve":
            return PayrollDetailSerializer

        return PayrollSerializer

    def perform_create(self, serializer):
        employee = self.request.user.employee

        payroll = PayrollService.create_payroll(
            employee=employee,
            year=serializer.validated_data["year"],
            month=serializer.validated_data["month"],
            basic_salary=serializer.validated_data["basic_salary"],
            allowance=serializer.validated_data["allowance"],
            deduction=serializer.validated_data["deduction"],
        )

        serializer.instance = payroll

    @action(detail=True, methods=["post"])
    def mark_paid(self, request, pk=None):
        payroll = self.get_object()

        if payroll.is_paid:
            return Response(
                {"detail": "Payroll has already been paid."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        payroll = PayrollService.mark_paid(payroll)

        serializer = PayrollDetailSerializer(payroll)

        return Response(serializer.data)

    
