from rest_framework.response import Response
from rest_framework import status

from base.views.company_base_view_set import CompanyBaseViewSet
from travel.models.travel_request import TravelRequest
from travel.serializers.travel_request_serializer import (
    TravelRequestDetailSerializer,
    TravelRequestListSerializer,
    TravelRequestSerializer,
)


class TravelRequestViewSet(CompanyBaseViewSet):
    queryset = TravelRequest.objects.all()
    serializer_class = TravelRequestSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        request_status = self.request.query_params.get("status")
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        if request_status:
            queryset = queryset.filter(status=request_status)

        if start_date:
            queryset = queryset.filter(end_date__date__gte=start_date)

        if end_date:
            queryset = queryset.filter(start_date__date__lte=end_date)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return TravelRequestListSerializer

        if self.action == "retrieve":
            return TravelRequestDetailSerializer

        return TravelRequestSerializer

    def perform_create(self, serializer):
        serializer.save(employee=self.request.user.employee, company=self.get_company())

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        response_serializer = TravelRequestDetailSerializer(
            serializer.instance,
            context=self.get_serializer_context(),
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )
