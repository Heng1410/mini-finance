from django.db import models

from base.models.company_base_model import CompanyBaseModel
from travel.models.travel_request import TravelRequest


class TravelExpense(CompanyBaseModel):
    travel_request = models.ForeignKey(
        TravelRequest,
        on_delete=models.PROTECT,
        related_name="expenses",
    )

    expense_date = models.DateField()
    category = models.CharField(max_length=50)
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    description = models.TextField(
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "travel_expense"
