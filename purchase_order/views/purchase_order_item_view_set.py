from rest_framework.response import Response
from rest_framework import status

from base.views.company_base_view_set import CompanyBaseViewSet
from purchase_order.models.purchase_order_item import PurchaseOrderItem
from purchase_order.serializers.purchase_order_item_serializer import (
    PurchaseOrderItemDetailSerializer,
    PurchaseOrderItemListSerializer,
    PurchaseOrderItemSerializer,
)
from purchase_order.services.purchase_order_service import PurchaseOrderService


class PurchaseOrderItemViewSet(CompanyBaseViewSet):
    queryset = PurchaseOrderItem.objects.all()
    serializer_class = PurchaseOrderItemSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return PurchaseOrderItemListSerializer

        if self.action == "retrieve":
            return PurchaseOrderItemDetailSerializer

        return PurchaseOrderItemSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        purchase_order_item = PurchaseOrderService.add_item(
            company=self.get_company(),
            purchase_order=serializer.validated_data["purchase_order"],
            product=serializer.validated_data["product"],
            quantity=serializer.validated_data["quantity"],
            unit_price=serializer.validated_data["unit_price"],
        )

        response_serializer = PurchaseOrderItemDetailSerializer(purchase_order_item)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )
