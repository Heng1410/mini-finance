from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from base.views.company_base_view_set import CompanyBaseViewSet
from case_support.models.case import Case
from case_support.serializers.case_assign_serializer import CaseAssignSerializer
from case_support.serializers.case_resolve_serializer import CaseResolveSerializer
from case_support.serializers.case_serializer import (
    CaseDetailSerializer,
    CaseListSerializer,
    CaseSerializer,
)
from case_support.services.case_service import CaseService


class CaseViewSet(CompanyBaseViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return CaseListSerializer
        if self.action == "retrieve":
            return CaseDetailSerializer
        return CaseSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        case = CaseService.create_case(
            company=self.get_company(),
            title=serializer.validated_data["title"],
            description=serializer.validated_data["description"],
            priority=serializer.validated_data["priority"],
            customer=serializer.validated_data["customer"],
        )

        response_serializer = CaseDetailSerializer(case)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def assign(self, request, pk=None):
        serializer = CaseAssignSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        case = self.get_object()
        employee = serializer.validated_data["employee"]

        case = CaseService.assign_case(
            company=self.get_company(),
            case=case,
            employee=employee,
        )

        response_serializer = CaseDetailSerializer(case)

        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def start(self, request, pk=None):
        case = self.get_object()

        case = CaseService.start_case(
            company=self.get_company(),
            case=case,
        )

        response_serializer = CaseDetailSerializer(case)

        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def resolve(self, request, pk=None):
        serializer = CaseResolveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        case = self.get_object()

        case = CaseService.resolve_case(
            company=self.get_company(),
            case=case,
            resolution_note=serializer.validated_data["resolution_note"],
        )

        response_serializer = CaseDetailSerializer(case)

        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def close(self, request, pk=None):
        case = self.get_object()

        case = CaseService.close_case(company=self.get_company(), case=case)

        response_serializer = CaseDetailSerializer(case)

        return Response(response_serializer.data, status=status.HTTP_200_OK)
