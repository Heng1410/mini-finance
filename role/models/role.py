from django.db import models

from base.models.base_model import BaseModel
from company.models.company import Company


# Create your models here.
class Role(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="roles")
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=32)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "roles"
        constraints = [
            models.UniqueConstraint(
                fields=["company", "code"], name="uq_company_roles_code"
            ),
            models.UniqueConstraint(
                fields=["company", "name"], name="uq_company_roles_name"
            ),
        ]
