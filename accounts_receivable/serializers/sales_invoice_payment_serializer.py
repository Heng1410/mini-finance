from rest_framework import serializers

from account.models.account import Account
from accounts_receivable.constants import InvoiceStatus
from accounts_receivable.models.sales_invoice import SalesInvoice
from accounts_receivable.models.sales_invoice_payment import SalesInvoicePayment
from base.serializers.base_serializer import BaseSerializer


class SalesInvoicePaymentSerializer(BaseSerializer):
    invoice = serializers.PrimaryKeyRelatedField(queryset=SalesInvoice.objects.all())
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    amount = serializers.DecimalField(max_digits=18, decimal_places=2, min_value=0.01)

    class Meta:
        model = SalesInvoicePayment
        fields = ("invoice", "payment_date", "amount", "account", "remarks")

    def validate(self, attrs):
        validated_data = super().validate(attrs)

        invoice = validated_data["invoice"]

        if invoice.status != InvoiceStatus.APPROVED:
            raise serializers.ValidationError(
                {"invoice": "Only approved invoices can receive payment."}
            )

        return validated_data
