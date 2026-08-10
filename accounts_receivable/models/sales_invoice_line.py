from django.db import models

from accounts_receivable.models.sales_invoice import SalesInvoice
from base.models.base_model import BaseModel


class SalesInvoiceLine(BaseModel):
    sales_invoice = models.ForeignKey(
        SalesInvoice, on_delete=models.CASCADE, related_name="lines"
    )
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=18, decimal_places=2)
    unit_price = models.DecimalField(max_digits=18, decimal_places=2)
    line_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
