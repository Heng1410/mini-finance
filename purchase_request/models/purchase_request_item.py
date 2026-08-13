from django.db import models

from base.models.company_base_model import CompanyBaseModel
from inventory.models.products import Product
from purchase_request.models.purchase_request import PurchaseRequest


class PurchaseRequestItem(CompanyBaseModel):
    purchase_request = models.ForeignKey(
        PurchaseRequest, on_delete=models.PROTECT, related_name="items"
    )

    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="purchase_request_items"
    )

    quantity = models.PositiveIntegerField()

    estimated_unit_price = models.DecimalField(max_digits=15, decimal_places=2)

    estimated_subtotal = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        db_table = "purchase_request_items"
