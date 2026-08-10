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

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        invoice = self.get_object()

        invoice = SalesInvoiceService.approve(invoice=invoice)
        
        response_serializer = SalesInvoiceDetailSerializer(invoice)

        return Response(response_serializer.data, status=status.HTTP_200_OK)
