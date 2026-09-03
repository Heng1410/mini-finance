from decimal import Decimal

from rest_framework import serializers

from base.serializers.base_serializer import BaseSerializer
from currency.models.exchange_rate_detail import ExchangeRateDetail
from currency.serializers.currency_serializer import CurrencyListSerializer
from currency.serializers.rate_category_serializer import RateCategoryListSerializer


class ExchangeRateDetailSerializer(BaseSerializer):
    rate_value = serializers.DecimalField(
        max_digits=40,
        decimal_places=20,
        read_only=True,
    )

    rate_reciprocal = serializers.DecimalField(
        max_digits=50,
        decimal_places=32,
        read_only=True,
    )

    class Meta:
        model = ExchangeRateDetail
        fields = [
            "id",
            "exchange_rate",
            "from_currency",
            "effective_date",
            "rate_category",
            "rate",
            "multi_or_divide",
            "rate_value",
            "rate_reciprocal",
        ]

    def validate_exchange_rate(self, value):
        company = self.context["request"].user.employee.company

        if value.company_id != company.id:
            raise serializers.ValidationError(
                "Exchange rate does not belong to the current company."
            )

        return value

    def validate_from_currency(self, value):
        company = self.context["request"].user.employee.company

        if value.company_id != company.id:
            raise serializers.ValidationError(
                "Currency does not belong to the current company."
            )

        return value

    def validate_rate_category(self, value):
        company = self.context["request"].user.employee.company

        if value.company_id != company.id:
            raise serializers.ValidationError(
                "Rate category does not belong to the current company."
            )

        return value

    def validate_rate(self, value):
        if value <= 0:
            raise serializers.ValidationError("Rate must be greater than zero.")

        return value

    def validate(self, attrs):
        exchange_rate = attrs.get("exchange_rate")
        from_currency = attrs.get("from_currency")

        if exchange_rate and from_currency:
            if exchange_rate.to_currency_id == from_currency.id:
                raise serializers.ValidationError(
                    {
                        "from_currency": (
                            "From currency cannot be the same as "
                            "the exchange rate's to currency."
                        )
                    }
                )

        return attrs

    def _calculate_rate_fields(self, validated_data):
        rate = validated_data["rate"]

        validated_data["rate_value"] = rate
        validated_data["rate_reciprocal"] = Decimal("1") / rate

        return validated_data

    def create(self, validated_data):
        validated_data = self._calculate_rate_fields(validated_data)

        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "rate" in validated_data:
            validated_data = self._calculate_rate_fields(validated_data)

        return super().update(instance, validated_data)


class ExchangeRateDetailListSerializer(BaseSerializer):
    rate_category = RateCategoryListSerializer(read_only=True)
    from_currency = CurrencyListSerializer(read_only=True)

    class Meta:
        model = ExchangeRateDetail
        fields = [
            "id",
            "exchange_rate",
            "from_currency",
            "effective_date",
            "rate_category",
            "rate",
            "multi_or_divide",
            "rate_value",
            "rate_reciprocal",
        ]


class ExchangeRateDetailDetailSerializer(ExchangeRateDetailSerializer):
    rate_category = RateCategoryListSerializer(read_only=True)
    from_currency = CurrencyListSerializer(read_only=True)
