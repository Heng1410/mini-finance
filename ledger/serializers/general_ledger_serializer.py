from rest_framework import serializers


class GeneralLedgerSerializer(serializers.Serializer):
    date = serializers.DateField()
    journal_no = serializers.CharField()
    description = serializers.CharField(allow_blank=True, allow_null=True)
    debit = serializers.DecimalField(
        max_digits=18,
        decimal_places=2,
    )
    credit = serializers.DecimalField(
        max_digits=18,
        decimal_places=2,
    )
