from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from base.views.company_base_view_set import CompanyBaseViewSet
from delivery.models.delivery_item import DeliveryItem
from delivery.models.delivery import Delivery
from delivery.serializers.delivery_item_serializer import (
    DeliveryItemDetailSerializer,
    DeliveryItemListSerializer,
    DeliveryItemSerializer,
)
from delivery.serializers.delivery_serializer import (
    DeliveryDetailSerializer,
    DeliveryListSerializer,
    DeliverySerializer,
)
from accounts_receivable.serializers.create_invoice_from_delivery_serializer import (
    CreateInvoiceFromDeliverySerializer,
)
from accounts_receivable.serializers.sales_invoice_serializer import (
    SalesInvoiceDetailSerializer,
)
from delivery.services.delivery_service import DeliveryService
from accounts_receivable.services.sales_invoice_service import SalesInvoiceService


class DeliveryViewSet(CompanyBaseViewSet):
    model = Delivery
    serializer_class = DeliverySerializer
    queryset = Delivery.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return DeliveryListSerializer

        if self.action == "retrieve":
            return DeliveryDetailSerializer

        return DeliverySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        delivery = DeliveryService.create_delivery(
            company=self.get_company(),
            sales_order=serializer.validated_data["sales_order"],
            delivery_date=serializer.validated_data["delivery_date"],
            employee=request.user.employee,
            notes=serializer.validated_data.get("notes", ""),
        )

        response_serializer = DeliveryDetailSerializer(
            delivery,
            context=self.get_serializer_context(),
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=True,
        methods=["get", "post"],
        url_path="items",
    )
    def items(self, request, pk=None):
        delivery = self.get_object()

        if request.method == "GET":
            items = delivery.items.all()

            serializer = DeliveryItemListSerializer(
                items,
                many=True,
                context=self.get_serializer_context(),
            )

            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

        serializer = DeliveryItemSerializer(
            data=request.data,
            context=self.get_serializer_context(),
        )

        serializer.is_valid(raise_exception=True)

        item = DeliveryService.add_item(
            company=self.get_company(),
            delivery=delivery,
            sales_order_item=serializer.validated_data["sales_order_item"],
            quantity=serializer.validated_data["quantity"],
        )

        response_serializer = DeliveryItemDetailSerializer(
            item,
            context=self.get_serializer_context(),
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["get", "post"], url_path="confirm")
    def confirm(self, request, pk=None):
        delivery = self.get_object()

        if request.method == "GET":
            serializer = DeliveryDetailSerializer(
                delivery,
                context=self.get_serializer_context(),
            )

            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

        delivery = DeliveryService.confirm_delivery(
            company=self.get_company(),
            delivery=delivery,
            employee=request.user.employee,
        )

        serializer = DeliveryDetailSerializer(
            delivery, context=self.get_serializer_context()
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="invoice")
    def invoice(self, request, pk=None):
        delivery = self.get_object()

        serializer = CreateInvoiceFromDeliverySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        invoice = SalesInvoiceService.create_from_delivery(
            company=self.get_company(),
            delivery=delivery,
            invoice_date=serializer.validated_data["invoice_date"],
            due_date=serializer.validated_data["due_date"],
            remarks=serializer.validated_data.get("remarks", ""),
        )

        response_serializer = SalesInvoiceDetailSerializer(
            invoice, context=self.get_serializer_context()
        )

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
