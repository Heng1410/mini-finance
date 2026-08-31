from django.utils import timezone
from rest_framework import serializers

from base.serializers.base_serializer import BaseSerializer
from transport.models.transport_expense import TransportExpense
from transport.serializers.transport_serializer import TransportSimpleSerializer


class TransportExpenseSerializer(BaseSerializer):
    class Meta:
        model = TransportExpense
        fields = [
            "id",
            "transport",
            "expense_type",
            "amount",
            "expense_date",
            "reference",
            "description",
        ]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Expense amount must be greater than zero."
            )
        return value

    def validate_expense_date(self, value):
        if value > timezone.localdate():
            raise serializers.ValidationError("Expense date cannot be in the future.")
        return value


class TransportExpenseListSerializer(BaseSerializer):
    transport = TransportSimpleSerializer(read_only=True)

    class Meta:
        model = TransportExpense
        fields = [
            "id",
            "transport",
            "expense_type",
            "amount",
            "expense_date",
            "reference",
        ]


class TransportExpenseDetailSerializer(TransportExpenseSerializer):
    transport = TransportSimpleSerializer(read_only=True)
