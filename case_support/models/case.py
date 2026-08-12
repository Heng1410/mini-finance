from django.db import models

from accounts_receivable.models.customer import Customer
from base.models.company_base_model import CompanyBaseModel
from case_support.constants import CasePriority, CaseStatus
from employee.models.employee import Employee


class Case(CompanyBaseModel):
    case_number = models.CharField(max_length=50)

    title = models.CharField(max_length=255)

    description = models.TextField()

    status = models.CharField(
        max_length=20, choices=CaseStatus.choices, default=CaseStatus.OPEN
    )

    priority = models.CharField(
        max_length=20, choices=CasePriority.choices, default=CasePriority.MEDIUM
    )

    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, related_name="cases"
    )

    assigned_to = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="assigned_cases",
        null=True,
        blank=True,
    )
    
    resolution_note = models.TextField(
        blank=True
    )

    class Meta:
        db_table = "cases"
        constraints = [
            models.UniqueConstraint(
                fields=["company", "case_number"], name="uq_case_number_per_company"
            )
        ]
