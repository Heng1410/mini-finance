from rest_framework.response import Response
from rest_framework import status

from base.views.company_base_view_set import CompanyBaseViewSet
from purchase_request.models.purchase_request_item import PurchaseRequestItem
from purchase_request.serializers.purchase_request_item_serializer import (
    PurchaseRequestItemDetailSerializer,
    PurchaseRequestItemListSerializer,
    PurchaseRequestItemSerializer,
)
from purchase_request.services.purchase_request_service import PurchaseRequestService


class PurchaseRequestItemViewSet(CompanyBaseViewSet):
    queryset = PurchaseRequestItem.objects.all()
    serializer_class = PurchaseRequestItemSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return PurchaseRequestItemListSerializer

        if self.action == "retrieve":
            return PurchaseRequestItemDetailSerializer

        return PurchaseRequestItemSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request_item = PurchaseRequestService.add_item(
            company=self.get_company(),
            request=serializer.validated_data["purchase_request"],
            product=serializer.validated_data["product"],
            quantity=serializer.validated_data["quantity"],
            estimated_unit_price=serializer.validated_data["estimated_unit_price"],
        )

        response_serializer = PurchaseRequestItemDetailSerializer(request_item)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )
