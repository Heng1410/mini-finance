from django.db import models

from accounts_receivable.models.customer import Customer
from base.models.company_base_model import CompanyBaseModel
from employee.models.employee import Employee
from sales_order.constants import SalesOrderStatus


class SalesOrder(CompanyBaseModel):
    order_number = models.CharField(max_length=50)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="sales_orders",
    )
    status = models.CharField(
        max_length=20, choices=SalesOrderStatus, default=SalesOrderStatus.DRAFT
    )
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    created_by = models.ForeignKey(
        Employee, on_delete=models.PROTECT, related_name="created_sales_orders"
    )

    class Meta:
        db_table = "sales_order"
        constraints = [
            models.UniqueConstraint(
                fields=["company", "order_number"], name="uq_order_number_per_company"
            )
        ]
