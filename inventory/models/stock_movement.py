from django.db import models
from django.db.models import Q

from base.models.company_base_model import CompanyBaseModel
from employee.models.employee import Employee
from inventory.constants import StockMovementType
from inventory.models.products import Product


class StockMovement(CompanyBaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="stock_movements"
    )

    movement_type = models.CharField(max_length=20, choices=StockMovementType.choices)
    quantity = models.BigIntegerField()

    performed_by = models.ForeignKey(
        Employee, on_delete=models.PROTECT, related_name="stock_movements"
    )

    reference = models.CharField(max_length=128, blank=True)
    note = models.TextField(
        blank=True,
    )

    class Meta:
        db_table = "stock_movements"
        constraints = [
            models.CheckConstraint(
                condition=Q(quantity__gt=0), name="ck_stock_movement_quantity_positive"
            )
        ]
