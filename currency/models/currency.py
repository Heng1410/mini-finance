from django.db import models

from base.models.company_base_model import CompanyBaseModel
from company.models.company import Company


class Currency(CompanyBaseModel):
    code = models.CharField(
        max_length=3,
    )

    name = models.CharField(
        max_length=100,
    )

    symbol = models.CharField(
        max_length=10,
        blank=True,
    )

    decimal_places = models.PositiveSmallIntegerField(
        default=2,
    )
    
    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        editable=False,
        related_name="currency_records",
    )

    class Meta:
        db_table = "currencies"
        constraints = [
            models.UniqueConstraint(
                fields=["company", "code"],
                name="unique_currency_code_per_company",
            ),
        ]
        indexes = [
            models.Index(
                fields=["company", "code"],
                name="currency_company_code_idx",
            ),
        ]