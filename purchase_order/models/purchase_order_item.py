from django.db import models

from base.models.company_base_model import CompanyBaseModel
from inventory.models.products import Product
from purchase_order.models.purchase_order import PurchaseOrder


class PurchaseOrderItem(CompanyBaseModel):
    purchase_order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.PROTECT,
        related_name="items",
    )

    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="purchase_order_items"
    )

    quantity = models.PositiveIntegerField()

    unit_price = models.DecimalField(max_digits=5, decimal_places=2)

    sub_total = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        db_table = "purchase_order_items"
