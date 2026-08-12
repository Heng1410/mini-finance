from django.db import models

from base.models.company_base_model import CompanyBaseModel
from inventory.models.products import Product
from sales_order.models.sales_order import SalesOrder


class SalesOrderItem(CompanyBaseModel):
    sales_order = models.ForeignKey(
        SalesOrder, on_delete=models.PROTECT, related_name="sales_order_items"
    )

    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="sales_product_items"
    )

    quantity = models.IntegerField()

    unit_price = models.DecimalField(max_digits=15, decimal_places=2)

    sub_total = models.DecimalField(
        max_digits=15,
        decimal_places=2,
    )

    class Meta:
        db_table = "sales_order_items"
