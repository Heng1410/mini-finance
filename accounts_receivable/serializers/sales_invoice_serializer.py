from rest_framework import serializers

from accounts_receivable.models.sales_invoice import SalesInvoice
from accounts_receivable.serializers.customer_serializer import CustomerListSerializer
from accounts_receivable.serializers.sales_invoice_line_serializer import (
    SalesInvoiceLineDetailSerializer,
    SalesInvoiceLineSerializer,
)
from base.serializers.base_serializer import BaseSerializer
from accounts_receivable.models.customer import Customer


class SalesInvoiceSerializer(BaseSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    lines = SalesInvoiceLineSerializer(many=True)

    class Meta:
        model = SalesInvoice
        fields = ("customer", "invoice_date", "due_date", "remarks", "lines")


class SalesInvoiceListSerializer(BaseSerializer):
    customer = CustomerListSerializer(read_only=True)

    class Meta:
        model = SalesInvoice
        fields = (
            "id",
            "customer",
            "invoice_no",
            "invoice_date",
            "due_date",
            "status",
            "total",
        )


class SalesInvoiceDetailSerializer(BaseSerializer):
    customer = CustomerListSerializer(read_only=True)
    lines = SalesInvoiceLineDetailSerializer(read_only=True, many=True)

    class Meta:
        model = SalesInvoice
        fields = (
            "id",
            "customer",
            "invoice_no",
            "invoice_date",
            "due_date",
            "status",
            "remarks",
            "total",
            "lines",
        )
