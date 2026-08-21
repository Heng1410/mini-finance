from django.db import models

from base.models.company_base_model import CompanyBaseModel
from employee.models.employee import Employee
from travel.models.travel_request import TravelRequest


class TravelRequestApproval(CompanyBaseModel):
    travel_request = models.ForeignKey(
        TravelRequest,
        on_delete=models.PROTECT,
        related_name="approvals",
    )

    approved_by = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="travel_request_approvals",
    )

    approved_at = models.DateTimeField(auto_now_add=True)

    remarks = models.TextField(
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "travel_request_approval"
        constraints = [
            models.UniqueConstraint(
                fields=["company", "travel_request", "approved_by"],
                name="uq_travel_request_approval",
            )
        ]
