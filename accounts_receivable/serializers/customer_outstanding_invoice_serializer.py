from rest_framework import serializers

from accounts_receivable.models.sales_invoice import SalesInvoice
from base.serializers.base_serializer import BaseSerializer


class CustomerOutstandingInvoiceSerializer(BaseSerializer):
    paid = serializers.DecimalField(max_digits=18, decimal_places=2)
    outstanding = serializers.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        model = SalesInvoice
        fields = (
            "id",
            "invoice_no",
            "invoice_date",
            "due_date",
            "total",
            "paid",
            "outstanding",
        )
