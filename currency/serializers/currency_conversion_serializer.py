from decimal import Decimal

from rest_framework import serializers

from base.serializers.base_serializer import BaseSerializer


class CurrencyConversionSerializer(BaseSerializer):
    amount = serializers.DecimalField(
        max_digits=20,decimal_places=6,min_value=Decimal("0")
    )
    
    from_currency = serializers.CharField(
        max_length=3
    )
    
    to_currency = serializers.CharField(
        max_length=3
    )
    
    effective_date = serializers.DateField(
        required=False
    )
    
    rate_category = serializers.CharField(
        required=False,
        allow_blank=False,max_length=50
    )
    
    def validate_from_currency(self,value):
        return value.upper()
    
    def validate_to_currency(self,value):
        return value.upper()