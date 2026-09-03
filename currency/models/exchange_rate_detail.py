from django.db import models

from base.models.company_base_model import CompanyBaseModel
from currency.models.currency import Currency
from currency.models.exchange_rate import ExchangeRate
from currency.models.rate_category import RateCategory


class ExchangeRateDetail(CompanyBaseModel):

    class RateOperation(models.TextChoices):
        MULTIPLY = "multi", "Multiply"
        DIVIDE = "divide", "Divide"

    exchange_rate = models.ForeignKey(
        ExchangeRate,
        on_delete=models.CASCADE,
        related_name="details",
    )

    from_currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        related_name="exchange_rate_details",
    )

    effective_date = models.DateField()

    rate_category = models.ForeignKey(
        RateCategory,
        on_delete=models.PROTECT,
        related_name="exchange_rate_details",
    )

    rate = models.DecimalField(
        max_digits=30,
        decimal_places=14,
    )

    multi_or_divide = models.CharField(
        max_length=10,
        choices=RateOperation.choices,
        default=RateOperation.MULTIPLY,
    )

    rate_value = models.DecimalField(
        max_digits=40,
        decimal_places=20,
    )

    rate_reciprocal = models.DecimalField(
        max_digits=50,
        decimal_places=32,
    )

    class Meta:
        db_table = "exchange_rate_details"
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "exchange_rate",
                    "from_currency",
                    "effective_date",
                    "rate_category",
                ],
                name="unique_exchange_rate_detail",
            ),
        ]
        indexes = [
            models.Index(
                fields=[
                    "from_currency",
                    "effective_date",
                ],
                name="exrate_detail_from_date_idx",
            ),
            models.Index(
                fields=[
                    "effective_date",
                    "rate_category",
                ],
                name="exrate_detail_date_cat_idx",
            ),
        ]
