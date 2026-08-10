from django.db import models

from base.models.company_base_model import CompanyBaseModel


# Create your models here.
class Customer(CompanyBaseModel):
    code = models.CharField(max_length=32, db_index=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=32)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "customers"
        ordering = ("code",)
        constraints = [
            models.UniqueConstraint(fields=["company", "code"], name="uq_customer_code")
        ]
