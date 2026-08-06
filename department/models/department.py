from django.db import models

from base.models.base_model import BaseModel
from company.models.company import Company


# Create your models here.
class Department(BaseModel):
    company = models.ForeignKey(
        Company, on_delete=models.PROTECT, related_name="departments"
    )
    name = models.CharField(
        max_length=255,
    )
    code = models.CharField(
        max_length=16,
    )
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "departments"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["company", "code"],
                name="uq_department_company_code",
            ),
            models.UniqueConstraint(
                fields=["company", "name"],
                name="uq_department_company_name",
            ),
        ]
