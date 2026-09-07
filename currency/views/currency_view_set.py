from rest_framework.decorators import action
from rest_framework.response import Response

from base.views.company_base_view_set import CompanyBaseViewSet
from currency.models.currency import Currency
from currency.serializers.currency_conversion_serializer import (
    CurrencyConversionSerializer,
)
from currency.serializers.currency_serializer import (
    CurrencyDetailSerializer,
    CurrencyListSerializer,
    CurrencySerializer,
)
from currency.services.currency_conversion_service import CurrencyConversionService


class CurrencyViewSet(CompanyBaseViewSet):
    model = Currency
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

    def get_serializer_class(self):
        if self.action == "list":
            return CurrencyListSerializer
        if self.action == "retrieve":
            return CurrencyDetailSerializer
        return CurrencySerializer

    @action(detail=False, methods=["get"], url_path="convert")
    def convert(self, request):
        serializer = CurrencyConversionSerializer(data=request.query_params)

        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        company = self.get_company()

        rate = CurrencyConversionService.get_rate(
            company=company,
            from_currency=data["from_currency"],
            to_currency=data["to_currency"],
            effective_date=data.get("effective_date"),
            rate_category=data.get("rate_category"),
        )

        converted_amount = CurrencyConversionService.convert(
            company=company, amount=data["amount"], from_currency=data["currency"]
        )

        return Response(
            {
                "from_currency": data["from_currency"],
                "to_currency": data["to_currency"],
                "amount": data["amount"],
                "rate": rate,
                "converted_amount": converted_amount,
            }
        )
