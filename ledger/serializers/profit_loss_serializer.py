from rest_framework import serializers


class ProfitLossItemSerializer(serializers.Serializer):
    code = serializers.CharField()
    name = serializers.CharField()
    balance = serializers.DecimalField(max_digits=18, decimal_places=2)
    
class ProfitLossSerializer(serializers.Serializer):
    revenue = ProfitLossItemSerializer(many=True)
    total_revenue = serializers.DecimalField(max_digits=18, decimal_places=2)
    
    expenses = ProfitLossItemSerializer(many=True)
    total_expenses = serializers.DecimalField(max_digits=18, decimal_places=2)
    
    net_profit = serializers.DecimalField(max_digits=18, decimal_places=2)
    
