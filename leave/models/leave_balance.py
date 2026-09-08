from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from base.models.company_base_model import CompanyBaseModel
from employee.models.employee import Employee
from leave.models.leave_type import LeaveType


class LeaveBalance(CompanyBaseModel):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="leave_balances",
    )
    leave_type = models.ForeignKey(
        LeaveType,
        on_delete=models.PROTECT,
        related_name="leave_balances",
    )
    year = models.PositiveIntegerField()

    allocated_days = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=Decimal("0"),
        validators=[MinValueValidator(Decimal("0"))],
    )

    used_days = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=Decimal("0"),
        validators=[MinValueValidator(Decimal("0"))],
    )

    class Meta:
        ordering = ["-year", "employee", "leave_type"]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "company",
                    "employee",
                    "leave_type",
                    "year",
                ],
                name="unique_leave_balance_per_employee_type_year",
            ),
        ]
