from rest_framework.decorators import action
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import FormParser, MultiPartParser

from base.views.company_base_view_set import CompanyBaseViewSet
from employee.models.employee import Employee
from employee_document.models.employee_document import EmployeeDocument
from employee_document.serializers.employee_document_serializer import (
    EmployeeDocumentDetailSerializer,
    EmployeeDocumentListSerializer,
    EmployeeDocumentSerializer,
)
from employee_document.services.employee_document_service import EmployeeDocumentService


class EmployeeDocumentViewSet(CompanyBaseViewSet):
    model = EmployeeDocument

    queryset = EmployeeDocument.objects.select_related("employee")

    serializer_class = EmployeeDocumentSerializer

    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    filter_backends = CompanyBaseViewSet.filter_backends + (DjangoFilterBackend,)

    filterset_fields = {
        "employee": ["exact"],
        "document_type": ["exact"],
        "issued_date": ["exact", "gte", "lte"],
        "expiry_date": ["exact", "gte", "lte"],
    }

    search_fields = [
        "employee__first_name",
        "employee__last_name",
        "name",
        "description",
    ]

    def get_serializer_class(self):
        if self.action == "list":
            return EmployeeDocumentListSerializer

        if self.action == "retrieve":
            return EmployeeDocumentDetailSerializer

        return EmployeeDocumentSerializer

    def perform_create(self, serializer):
        serializer.save(
            company=self.get_company(),
            employee=self.request.user.employee,
        )
        
    def perform_destroy(self, instance):
        EmployeeDocumentService.delete_document(instance)

    @action(detail=False, methods=["get"])
    def expiring_soon(self, request):
        try:
            days = int(request.query_params.get("days", 30))
        except ValueError:
            return Response(
                {"detail": "days must be a valid integer."},
                status=400,
            )

        if days < 0:
            return Response(
                {"detail": "days must be greater than or equal to 0."},
                status=400,
            )

        documents = EmployeeDocumentService.get_expiring_soon(
            company=self.get_company(),
            days=days,
        )

        serializer = EmployeeDocumentListSerializer(documents, many=True)

        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def exiring_soon(self, request):
        try:
            days = int(request.query_params.get("days", 30))
        except ValueError:
            return Response(
                {"detail": "days must be a valid integer."},
                status=400,
            )

        if days < 0:
            return Response(
                {"detail": "days must be greater than or equal to 0."},
                status=400,
            )

        documents = EmployeeDocumentService.get_expiring_soon(
            company=self.get_company(), days=days
        )

        serializer = EmployeeDocumentListSerializer(documents, many=True)

        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def expired(self, request):

        documents = EmployeeDocumentService.get_expired(company=self.get_company())

        serializer = EmployeeDocumentListSerializer(documents, many=True)

        return Response(serializer.data)
