from django.db import models

# Create your models here.
from account.constants import AccountRole, AccountType
from base.models.company_base_model import CompanyBaseModel


# Create your views here.
class Account(CompanyBaseModel):
    code = models.CharField(max_length=20, db_index=True)
    name = models.CharField(max_length=100, db_index=True)
    account_type = models.CharField(max_length=20, choices=AccountType.choices)
    parent = models.ForeignKey(
        "self", on_delete=models.PROTECT, related_name="children", null=True, blank=True
    )
    description = models.TextField(blank=True, null=True)
    role = models.CharField(
        max_length=30, choices=AccountRole.choices, null=True, blank=True
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "accounts"
        ordering = ["code"]
        constraints = [
            models.UniqueConstraint(
                fields=["company", "code"], name="uq_account_code_per_company"
            )
        ]
