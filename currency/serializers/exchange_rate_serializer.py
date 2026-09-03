from rest_framework import serializers

from base.serializers.base_serializer import BaseSerializer
from currency.models.exchange_rate import ExchangeRate
from currency.serializers.currency_serializer import CurrencyListSerializer
from currency.serializers.exchange_rate_detail_serializer import (
    ExchangeRateDetailListSerializer,
)


class ExchangeRateSerializer(BaseSerializer):
    class Meta:
        model = ExchangeRate
        fields = ["id", "to_currency"]

    def validate_to_currency(self, value):
        company = self.context["request"].user.employee.company

        if value.company_id != company.id:
            raise serializers.ValidationError(
                "Currency does not belong to the current company."
            )

        return value

    def validate(self, attrs):
        company = self.context["request"].user.employee.company
        to_currency = attrs.get("to_currency")

        if to_currency:
            queryset = ExchangeRate.objects.filter(
                company=company,
                to_currency=to_currency,
            )

            if self.instance:
                queryset = queryset.exclude(
                    pk=self.instance.pk,
                )

            if queryset.exists():
                raise serializers.ValidationError(
                    {
                        "to_currency": (
                            "An exchange rate for this currency "
                            "already exists for this company."
                        )
                    }
                )

        return attrs


class ExchangeRateListSerializer(BaseSerializer):
    details = ExchangeRateDetailListSerializer(
            many=True,
            read_only=True,
        )
    to_currency = CurrencyListSerializer(read_only=True)

    class Meta:
        model = ExchangeRate
        fields = ["id", "to_currency","details"]


class ExchangeRateDetailSerializer(ExchangeRateSerializer):
    details = ExchangeRateDetailListSerializer(
        many=True,
        read_only=True,
    )
    to_currency = CurrencyListSerializer(read_only=True)

    class Meta:
        model = ExchangeRate
        fields = [
            "id",
            "to_currency",
            "details",
        ]
