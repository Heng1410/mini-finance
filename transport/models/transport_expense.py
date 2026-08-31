from django.db import models

from base.models.company_base_model import CompanyBaseModel
from transport.constants import TransportExpenseType
from transport.models.transport import Transport


class TransportExpense(CompanyBaseModel):
    transport = models.ForeignKey(
        Transport, on_delete=models.PROTECT, related_name="expense"
    )

    expense_type = models.CharField(max_length=30, choices=TransportExpenseType.choices)

    amount = models.DecimalField(max_digits=15, decimal_places=2)

    expense_date = models.DateField()

    reference = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "transport_expense"
