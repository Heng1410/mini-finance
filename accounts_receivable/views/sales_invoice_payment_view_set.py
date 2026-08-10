from rest_framework import status
from rest_framework.response import Response

from accounts_receivable.models.sales_invoice_payment import SalesInvoicePayment
from accounts_receivable.serializers.sales_invoice_payment_serializer import (
    SalesInvoicePaymentSerializer,
)
from base.views.company_base_view_set import CompanyBaseViewSet
from accounts_receivable.services.sales_invoice_payment_service import (
    SalesInvoicePaymentService,
)


class SalesInvoicePaymentViewSet(CompanyBaseViewSet):
    queryset = SalesInvoicePayment.objects.all()
    serializer_class = SalesInvoicePaymentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        company = self.get_company()

        payment = SalesInvoicePaymentService.create(
            company=company, **serializer.validated_data
        )

        response_serializer = self.get_serializer(payment)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
