from rest_framework import serializers

from account.constants import AccountType


class BalanceSheetItemSerializer(serializers.Serializer):
    code = serializers.CharField()
    name = serializers.CharField()
    balance = serializers.DecimalField(max_digits=18, decimal_places=2)


class BalanceSheetSerializer(serializers.Serializer):
    assets = BalanceSheetItemSerializer(many=True)
    total_assets = serializers.DecimalField(max_digits=18, decimal_places=2)

    liabilities = BalanceSheetItemSerializer(many=True)
    total_liabilities = serializers.DecimalField(max_digits=18, decimal_places=2)

    equity = BalanceSheetItemSerializer(many=True)
    total_equity = serializers.DecimalField(max_digits=18, decimal_places=2)
