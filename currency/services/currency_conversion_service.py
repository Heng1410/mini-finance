from datetime import date
from decimal import Decimal
from currency.models.currency import Currency

from currency.models.exchange_rate_detail import ExchangeRateDetail


class CurrencyConversionService:
    @staticmethod
    def get_rate(
        company, from_currency, to_currency, effective_date=None, rate_category=None
    ):
        effective_date = effective_date or date.today()

        if from_currency == to_currency:
            return Decimal("1")

        detail = CurrencyConversionService._get_exchange_rate_detail(
            company=company,
            from_currency=from_currency,
            to_currency=to_currency,
            effective_date=effective_date,
            rate_category=rate_category,
        )

        if detail:
            return CurrencyConversionService._calculate_rate(detail)

        inverse_detail = CurrencyConversionService._get_exchange_rate_detail(
            company=company,
            from_currency=to_currency,
            to_currency=from_currency,
            effective_date=effective_date,
            rate_category=rate_category,
        )

        if not inverse_detail:
            raise ValueError(
                f"No exchange rate found for " f"{from_currency} -> {to_currency}"
            )

        return CurrencyConversionService._calculate_inverse_rate(inverse_detail)

    @staticmethod
    def convert(
        company,
        amount,
        from_currency,
        to_currency,
        effective_date=None,
        rate_category=None,
    ):
        amount = Decimal(str(amount))

        rate = CurrencyConversionService.get_rate(
            company=company,
            from_currency=from_currency,
            to_currency=to_currency,
            effective_date=effective_date,
            rate_category=rate_category,
        )

        converted_amount = amount * rate

        return CurrencyConversionService._round_amount(
            converted_amount, to_currency, company
        )

    @staticmethod
    def _get_exchange_rate_detail(
        company, from_currency, to_currency, effective_date, rate_category=None
    ):
        queryset = ExchangeRateDetail.objects.filter(
            exchange_rate__company=company,
            from_currency__code=from_currency,
            exchange_rate__to_currency=to_currency,
            effective_date__lte=effective_date,
        )

        if rate_category:
            queryset = queryset.filter(
                rate_category__code=rate_category,
            )

        return queryset.order_by("-effective_date").first()

    @staticmethod
    def _calculate_rate(detail):
        if detail.multi_or_divide == ExchangeRateDetail.RateOperation.MULTIPLY:
            return detail.rate_value

        return detail.rate_reciprocal

    @staticmethod
    def _calculate_inverse_rate(detail):
        rate = CurrencyConversionService._calculate_rate(detail)

        return Decimal("1") / rate

    @staticmethod
    def _round_amount(amount, currency_code, company):
        currency = Currency.objects.get(code=currency_code, company=company)

        quantizer = Decimal("1").scaleb(-currency.decimal_places)

        return amount.quantize(quantizer)
