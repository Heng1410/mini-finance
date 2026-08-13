from django.db import models

from base.models.company_base_model import CompanyBaseModel
from employee.models.employee import Employee
from purchase_request.constants import PurchaseRequestStatus


# Create your models here.
class PurchaseRequest(CompanyBaseModel):
    request_number = models.CharField(max_length=50)

    requested_by = models.ForeignKey(
        Employee, on_delete=models.PROTECT, related_name="purchase_requests"
    )

    title = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=PurchaseRequestStatus.choices,
        default=PurchaseRequestStatus.DRAFT,
    )

    approved_by = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="approved_purchase_requests",
    )

    rejected_by = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="rejected_purchase_requests",
    )

    rejected_reason = models.TextField(blank=True)

    class Meta:
        db_table = "purchase_requests"
        constraints = [
            models.UniqueConstraint(
                fields=["company", "request_number"],
                name="uq_purchase_request_number_per_company",
            )
        ]
