from django.db import models

from base.models.company_base_model import CompanyBaseModel


class RateCategory(CompanyBaseModel):
    code = models.CharField(
        max_length=50,
    )

    name = models.CharField(
        max_length=100,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    default = models.BooleanField(
        default=False,
    )

    is_nbc = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "rate_categories"
        constraints = [
            models.UniqueConstraint(
                fields=["company", "code"],
                name="unique_rate_category_code_per_company",
            ),
            models.UniqueConstraint(
                fields=["company"],
                condition=models.Q(default=True),
                name="unique_default_rate_category_per_company",
            ),
        ]
        indexes = [
            models.Index(
                fields=["company", "code"],
                name="rate_category_company_code_idx",
            ),
        ]