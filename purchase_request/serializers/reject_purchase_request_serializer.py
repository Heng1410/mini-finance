from rest_framework import serializers


class RejectPurchaseRequestSerializer(serializers.Serializer):
    rejection_reason = serializers.CharField(
        required=True,
        allow_blank=False,
    )
