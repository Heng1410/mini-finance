from rest_framework import serializers


class TrialBalanceSerializer(serializers.Serializer):
    code = serializers.CharField()
    name = serializers.CharField()
    debit = serializers.DecimalField(
        max_digits=18,
        decimal_places=2,
    )
    credit = serializers.DecimalField(
        max_digits=18,
        decimal_places=2,
    )
