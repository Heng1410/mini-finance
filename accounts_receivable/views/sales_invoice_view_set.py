from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from accounts_receivable.models.sales_invoice import SalesInvoice
from accounts_receivable.services.sales_invoice_service import SalesInvoiceService
from accounts_receivable.serializers.sales_invoice_serializer import (
    SalesInvoiceDetailSerializer,
    SalesInvoiceListSerializer,
    SalesInvoiceSerializer,
)
from base.views.company_base_view_set import CompanyBaseViewSet


class SalesInvoiceViewSet(CompanyBaseViewSet):
    queryset = SalesInvoice.objects.all()
    serializer_class = SalesInvoiceSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        company = self.get_company()

        invoice = SalesInvoiceService.create(
            company=company,
            **serializer.validated_data,
        )

        response_serializer = SalesInvoiceDetailSerializer(invoice)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if self.action == "list":
            return SalesInvoiceListSerializer

        if self.action == "retrieve":
            return SalesInvoiceDetailSerializer
        return SalesInvoiceSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        invoice_status = self.request.query_params.get("status")
        date_from = self.request.query_params.get("date_from")
        date_to = self.request.query_params.get("date_to")

        if invoice_status:
            queryset = queryset.filter(status=invoice_status)
        if date_from:
            queryset = queryset.filter(invoice_date__gte=date_from)
        if date_to:
            queryset = queryset.filter(invoice_date__lte=date_to)
        return queryset

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        invoice = self.get_object()

        invoice = SalesInvoiceService.approve(invoice=invoice)

        response_serializer = SalesInvoiceDetailSerializer(invoice)

        return Response(response_serializer.data, status=status.HTTP_200_OK)

