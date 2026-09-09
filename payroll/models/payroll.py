from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models

from base.models.company_base_model import CompanyBaseModel
from employee.models.employee import Employee


class Payroll(CompanyBaseModel):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="payrolls",
    )
    year = models.PositiveIntegerField()
    month = models.PositiveSmallIntegerField()

    basic_salary = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    allowance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    deduction = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    net_salary = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    is_paid = models.BooleanField(
        default=False,
        db_index=True,
    )
    paid_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-year", "-month"]
        constraints = [
            models.UniqueConstraint(
                fields=["company", "employee", "year", "month"],
                name="unique_payroll_per_employee_month",
            ),
        ]

    def clean(self):
        if not 1 <= self.month <= 12:
            raise ValidationError({"month": "Month must be between 1 and 12."})

        if self.basic_salary < 0:
            raise ValidationError({"basic_salary": "Basic salary cannot be negative."})

        if self.allowance < 0:
            raise ValidationError({"allowance": "Allowance cannot be negative."})

        if self.deduction < 0:
            raise ValidationError({"deduction": "Deduction cannot be negative."})
