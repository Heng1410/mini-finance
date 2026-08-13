from django.db import models

from base.models.company_base_model import CompanyBaseModel


class Supplier(CompanyBaseModel):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "suppliers"
        constraints = [
            models.UniqueConstraint(
                fields=["company", "code"],
                name="uq_supplier_code_per_company",
            )
        ]
