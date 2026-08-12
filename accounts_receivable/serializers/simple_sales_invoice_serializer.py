from accounts_receivable.models.sales_invoice import SalesInvoice
from base.serializers.base_serializer import BaseSerializer


class SimpleSalesInvoiceSerializer(BaseSerializer):
    class Meta:
        model = SalesInvoice
        fields = (
            "id",
            "invoice_no",
            "invoice_date",
            "due_date",
            "status",
            "total",
        )