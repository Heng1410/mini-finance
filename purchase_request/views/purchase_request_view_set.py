from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from base.views.company_base_view_set import CompanyBaseViewSet
from purchase_request.models.purchase_request import PurchaseRequest
from purchase_request.serializers.purchase_request_serializer import (
    PurchaseRequestDetailSerializer,
    PurchaseRequestListSerializer,
    PurchaseRequestSerializer,
)
from purchase_request.serializers.reject_purchase_request_serializer import (
    RejectPurchaseRequestSerializer,
)
from purchase_request.services.purchase_request_service import PurchaseRequestService


class PurchaseRequestViewSet(CompanyBaseViewSet):
    queryset = PurchaseRequest.objects.all()
    serializer_class = PurchaseRequestSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return PurchaseRequestListSerializer

        if self.action == "retrieve":
            return PurchaseRequestDetailSerializer

        return PurchaseRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request = PurchaseRequestService.create_request(
            company=self.get_company(),
            employee=request.user.employee,
            title=serializer.validated_data["title"],
            description=serializer.validated_data["description"],
        )
        response_serializer = PurchaseRequestDetailSerializer(request)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        purchase_request = self.get_object()

        purchase_request = PurchaseRequestService.submit_request(
            company=self.get_company(), request=purchase_request
        )

        response_serializer = PurchaseRequestDetailSerializer(purchase_request)

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        purchase_request = self.get_object()

        purchase_request = PurchaseRequestService.approve_request(
            company=self.get_company(),
            request=purchase_request,
            employee=request.user.employee,
        )

        response_serializer = PurchaseRequestDetailSerializer(purchase_request)

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        serializer = RejectPurchaseRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        purchase_request = self.get_object()

        purchase_request = PurchaseRequestService.reject_request(
            company=self.get_company(),
            request=purchase_request,
            employee=request.user.employee,
            rejection_reason=serializer.validated_data["rejection_reason"],
        )

        response_serializer = PurchaseRequestDetailSerializer(purchase_request)

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK,
        )
