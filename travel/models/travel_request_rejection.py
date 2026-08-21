from django.db import models

from base.models.company_base_model import CompanyBaseModel
from employee.models.employee import Employee
from travel.models.travel_request import TravelRequest


class TravelRequestRejection(CompanyBaseModel):
    travel_request = models.ForeignKey(
        TravelRequest,
        on_delete=models.PROTECT,
        related_name="rejections",
    )

    rejected_by = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="travel_request_rejections",
    )

    rejected_at = models.DateTimeField(auto_now_add=True)

    remarks = models.TextField(
        blank=True,
        null=True,
    )
    
    class Meta:
        db_table = "travel_request_rejection"
        