from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models

from base.models.company_base_model import CompanyBaseModel
from employee.models.employee import Employee
from expense.constants import ExpenseCategory, ExpenseStatus


class Expense(CompanyBaseModel):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="expenses",
    )
    date = models.DateField()
    category = models.CharField(
        max_length=30,
        choices=ExpenseCategory.choices,
    )
    description = models.CharField(max_length=255)
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
    )
    status = models.CharField(
        max_length=20,
        choices=ExpenseStatus.choices,
        default=ExpenseStatus.PENDING,
        db_index=True,
    )
    reimbursed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-date", "-created_at"]

    def clean(self):
        if self.amount <= Decimal("0.00"):
            raise ValidationError(
                {"amount": "Expense amount must be greater than zero."}
            )
