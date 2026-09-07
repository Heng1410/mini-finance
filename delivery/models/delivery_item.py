from django.db import models
from django.db.models import Q

from base.models.company_base_model import CompanyBaseModel
from delivery.models.delivery import Delivery
from inventory.models.products import Product
from sales_order.models.sales_order_item import SalesOrderItem


class DeliveryItem(CompanyBaseModel):
    delivery = models.ForeignKey(
        Delivery, on_delete=models.PROTECT, related_name="items"
    )

    sales_order_item = models.ForeignKey(
        SalesOrderItem, on_delete=models.PROTECT, related_name="delivery_items"
    )

    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="delivery_items"
    )

    quantity = models.DecimalField(max_digits=18, decimal_places=4)

    unit_price = models.DecimalField(max_digits=18, decimal_places=2)

    amount = models.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(quantity__gt=0),
                name="delivery_item_quantity_positive",
            ),
            models.CheckConstraint(
                condition=Q(unit_price__gte=0),
                name="delivery_item_unit_price_non_negative",
            ),
            models.CheckConstraint(
                condition=Q(amount__gte=0),
                name="delivery_item_amount_non_negative",
            ),
        ]