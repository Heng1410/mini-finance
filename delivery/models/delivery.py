from django.db import models

from base.models.company_base_model import CompanyBaseModel
from delivery.constants import DeliveryStatus
from employee.models.employee import Employee
from sales_order.models.sales_order import SalesOrder


class Delivery(CompanyBaseModel):
    delivery_number = models.CharField(max_length=50)

    sales_order = models.ForeignKey(
        SalesOrder, on_delete=models.PROTECT, related_name="deliveries"
    )

    status = models.CharField(
        max_length=20, choices=DeliveryStatus.choices, default=DeliveryStatus.DRAFT
    )

    delivery_date = models.DateField()

    created_by = models.ForeignKey(
        Employee, on_delete=models.PROTECT, related_name="created_deliveries"
    )

    confirmed_by = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="confirmed_deliveries",
        null=True,
        blank=True,
    )

    confirmed_at = models.DateTimeField(null=True, blank=True)

    notes = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["company", "delivery_number"],
                name="unique_delivery_number_per_company",
            ),
        ]
