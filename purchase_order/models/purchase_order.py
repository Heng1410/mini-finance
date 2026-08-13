from django.db import models

from base.models.company_base_model import CompanyBaseModel
from employee.models.employee import Employee
from purchase_order.constants import PurchaseOrderStatus
from purchase_request.models.purchase_request import PurchaseRequest
from supplier.models.supplier import Supplier


# Create your models here.
class PurchaseOrder(CompanyBaseModel):
    order_number = models.CharField(max_length=50)

    purchase_request = models.ForeignKey(
        PurchaseRequest, on_delete=models.PROTECT, related_name="purchase_orders"
    )

    supplier = models.ForeignKey(
        Supplier, on_delete=models.PROTECT, related_name="purchase_orders"
    )

    status = models.CharField(
        max_length=20,
        choices=PurchaseOrderStatus.choices,
        default=PurchaseOrderStatus.DRAFT,
    )

    total_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    created_by = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="created_purchase_orders",
    )

    class Meta:
        db_table = "purchase_orders"
        constraints = [
            models.UniqueConstraint(
                fields=["company", "order_number"],
                name="uq_purchase_order_number_per_company",
            )
        ]
