from django.db import models

from base.models.company_base_model import CompanyBaseModel
from currency.models.currency import Currency


class ExchangeRate(CompanyBaseModel):
    to_currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        related_name="exchange_rates",
    )

    class Meta:
        db_table = "exchange_rates"
        constraints = [
            models.UniqueConstraint(
                fields=["company", "to_currency"],
                name="unique_exchange_rate_currency_per_company",
            ),
        ]
        indexes = [
            models.Index(
                fields=["company", "to_currency"],
                name="exrate_company_curr_idx",
            ),
        ]
