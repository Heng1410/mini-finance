from rest_framework.response import Response
from rest_framework import status

from base.views.company_base_view_set import CompanyBaseViewSet
from sales_order.models.sales_order_item import SalesOrderItem
from sales_order.serializers.sales_order_item_serializer import (
    SalesOrderItemDetailSerializer,
    SalesOrderItemListSerializer,
    SalesOrderItemSerializer,
)
from sales_order.services.sales_order_service import SalesOrderService


class SalesOrderItemViewSet(CompanyBaseViewSet):
    queryset = SalesOrderItem.objects.all()
    serializer_class = SalesOrderItemSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return SalesOrderItemListSerializer
        if self.action == "retrieve":
            return SalesOrderItemDetailSerializer
        return SalesOrderItemSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_item = SalesOrderService.add_item(
            company=self.get_company(),
            quantity=serializer.validated_data["quantity"],
            order=serializer.validated_data["sales_order"],
            product=serializer.validated_data["product"],
            unit_price=serializer.validated_data["unit_price"],
        )

        response_serializer = SalesOrderItemDetailSerializer(order_item)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
