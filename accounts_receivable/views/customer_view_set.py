from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from base.views.company_base_view_set import CompanyBaseViewSet
from accounts_receivable.models.customer import Customer
from accounts_receivable.serializers.customer_serializer import (
    CustomerDetailSerializer,
    CustomerListSerializer,
    CustomerSerializer,
)
from accounts_receivable.services.customer_invoice_summary_service import (
    CustomerInvoiceSummaryService,
)
from accounts_receivable.services.customer_outstanding_invoices_service import (
    CustomerOutstandingInvoicesService,
)
from accounts_receivable.serializers.customer_outstanding_invoice_serializer import (
    CustomerOutstandingInvoiceSerializer,
)


class CustomerViewSet(CompanyBaseViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return CustomerListSerializer
        if self.action == "retrieve":
            return CustomerDetailSerializer
        return CustomerSerializer

    @action(
        detail=True,
        methods=["get"],
        url_path="summary-invoice",
    )
    def summary_invoice(self, request, pk=None):
        customer = self.get_object()

        summary = CustomerInvoiceSummaryService.get_summary(customer=customer)

        return Response(
            {
                "customer": {
                    "id": customer.id,
                    "code": customer.code,
                    "name": customer.name,
                    "phone": customer.phone,
                    "email": customer.email,
                    "address": customer.address,
                    "is_active": customer.is_active,
                },
                "summary": summary,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["get"], url_path="outstanding-invoices")
    def outstanding_invoices(self, request, pk=None):
        customer = self.get_object()

        invoices = CustomerOutstandingInvoicesService.get_outstanding_invoice(
            customer=customer
        )

        response_serializer = CustomerOutstandingInvoiceSerializer(invoices, many=True)

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK,
        )
