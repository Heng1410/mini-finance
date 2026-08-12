from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from base.views.company_base_view_set import CompanyBaseViewSet
from sales_order.models.sales_order import SalesOrder
from sales_order.serializers.sales_order_serializer import (
    SalesOrderDetailSerializer,
    SalesOrderListSerializer,
    SalesOrderSerializer,
)
from sales_order.services.sales_order_service import SalesOrderService


class SalesOrderViewSet(CompanyBaseViewSet):
    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return SalesOrderListSerializer
        if self.action == "retrieve":
            return SalesOrderDetailSerializer
        return SalesOrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = SalesOrderService.create_order(
            company=self.get_company(),
            customer=serializer.validated_data["customer"],
            employee=request.user.employee,
        )

        response_serializer = SalesOrderDetailSerializer(order)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        sales_order = self.get_object()

        sales_order = SalesOrderService.submit_order(
            company=self.get_company(),
            employee=request.user.employee,
            order=sales_order,
        )

        response_serializer = SalesOrderDetailSerializer(sales_order)

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def confirm(self, request, pk=None):
        sales_order = self.get_object()

        sales_order = SalesOrderService.confirm_order(
            company=self.get_company(),
            order=sales_order,
        )

        response_serializer = SalesOrderDetailSerializer(sales_order)
        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        sales_order = self.get_object()

        sales_order = SalesOrderService.cancel_order(
            company=self.get_company(),
            order=sales_order,
        )

        response_serializer = SalesOrderDetailSerializer(sales_order)

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK,
        )
