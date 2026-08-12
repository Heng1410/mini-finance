from django.db import models
from django.db.models import Q

from base.models.company_base_model import CompanyBaseModel
from employee.models.employee import Employee
from inventory.constants import StockReserveStatus
from inventory.models.products import Product


class StockReservation(CompanyBaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="stock_reservations"
    )
    quantity = models.BigIntegerField()
    status = models.CharField(
        max_length=20,
        choices=StockReserveStatus.choices,
        default=StockReserveStatus.PENDING,
    )
    reserved_by = models.ForeignKey(
        Employee, on_delete=models.PROTECT, related_name="stock_reservations"
    )
    reserved_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        db_table = "stock_reservations"
        constraints = [
            models.CheckConstraint(
                condition=Q(quantity__gt=0),
                name="ck_stock_reservation_quantity_positive",
            )
        ]
