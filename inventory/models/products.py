from django.db import models
from django.db.models import Q


from base.models.company_base_model import CompanyBaseModel


class Product(CompanyBaseModel):
    sku = models.CharField(max_length=12)
    name = models.CharField(max_length=128)
    stock_quantity = models.BigIntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "products"
        constraints = [
            models.UniqueConstraint(
                fields=["company", "sku"],
                name="uq_sku_per_company",
            ),
            models.CheckConstraint(
                condition=Q(stock_quantity__gte=0),
                name="ck_product_stock_non_negative",
            ),
        ]
