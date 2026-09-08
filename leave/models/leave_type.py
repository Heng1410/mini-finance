from decimal import Decimal
from django.core.validators import MinValueValidator

from django.db import models

from base.models.company_base_model import CompanyBaseModel


class LeaveType(CompanyBaseModel):
    code = models.CharField(
        max_length=32,
        db_index=True,
    )

    name = models.CharField(
        max_length=100,
    )

    description = models.CharField(
        max_length=255,
        blank=True,
    )

    days_per_year = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[
            MinValueValidator(Decimal("0")),
        ],
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = ["code"]
        constraints = [
            models.UniqueConstraint(
                fields=["company", "code"],
                name="unique_leave_type_code_per_company",
            ),
        ]
