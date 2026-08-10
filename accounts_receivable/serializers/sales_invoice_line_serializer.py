from rest_framework import serializers

from accounts_receivable.models.sales_invoice_line import SalesInvoiceLine
from base.serializers.base_serializer import BaseSerializer


class SalesInvoiceLineSerializer(BaseSerializer):
    quantity = serializers.DecimalField(
        max_digits=18,
        decimal_places=2,
        min_value=0.01,
    )
    unit_price = serializers.DecimalField(
        max_digits=18,
        decimal_places=2,
        min_value=0,
    )
    description = serializers.CharField(
        max_length=255,
        allow_blank=False,
    )

    class Meta:
        model = SalesInvoiceLine
        fields = (
            "description",
            "quantity",
            "unit_price",
        )


class SalesInvoiceLineListSerializer(BaseSerializer):
    class Meta:
        model = SalesInvoiceLine
        fields = (
            "id",
            "description",
            "quantity",
            "unit_price",
            "line_total",
        )
        read_only_fields = (
            "id",
            "line_total",
        )


class SalesInvoiceLineDetailSerializer(BaseSerializer):
    class Meta:
        model = SalesInvoiceLine
        fields = (
            "id",
            "description",
            "quantity",
            "unit_price",
            "line_total",
        )
        read_only_fields = (
            "id",
            "line_total",
        )
