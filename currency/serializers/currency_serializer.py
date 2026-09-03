from rest_framework import serializers

from base.serializers.base_serializer import BaseSerializer
from currency.models.currency import Currency


class CurrencySerializer(BaseSerializer):
    class Meta:
        model = Currency
        fields = [
            "id",
            "code",
            "name",
            "symbol",
            "decimal_places",
        ]

    def validate_code(self, value):
        value = value.strip().upper()

        if len(value) != 3 or not value.isalpha():
            raise serializers.ValidationError(
                "Currency code must contain exactly 3 letters."
            )

        return value

    def validate_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Currency name cannot be empty.")

        return value

    def validate_symbol(self, value):

        return value.strip()

    def validate_decimal_places(self, value):
        if value > 6:
            raise serializers.ValidationError("Decimal places cannot exceed 6.")

        return value

    def validate(self, attrs):
        company = self.context["request"].user.employee.company
        
        code = attrs.get("code")

        queryset = Currency.objects.filter(company=company, code=code)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                {
                    "code": (
                        "A currency with this code already exists "
                        "for this company."
                    )
                }
            )

        return attrs


class CurrencyListSerializer(BaseSerializer):
    class Meta:
        model = Currency
        fields = ["id", "code", "name", "symbol"]


class CurrencyDetailSerializer(CurrencySerializer):
    pass
