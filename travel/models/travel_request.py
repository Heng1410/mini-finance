from django.db import models

from base.models.company_base_model import CompanyBaseModel
from employee.models.employee import Employee
from travel.constants import TravelRequestStatus
from travel.models.destination import Destination


class TravelRequest(CompanyBaseModel):
    employee = models.ForeignKey(
        Employee, on_delete=models.PROTECT, related_name="travel_requests"
    )
    destination = models.ForeignKey(
        Destination, on_delete=models.PROTECT, related_name="travel_requests"
    )
    purpose = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=TravelRequestStatus.choices,
        default=TravelRequestStatus.DRAFT,
    )

    class Meta:
        db_table = "travel_request"
