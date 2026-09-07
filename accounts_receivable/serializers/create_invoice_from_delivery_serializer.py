from rest_framework import serializers


class CreateInvoiceFromDeliverySerializer(serializers.Serializer):
    invoice_date = serializers.DateField()
    due_date = serializers.DateField()
    remarks = serializers.CharField(required=False, allow_blank=True, default="")