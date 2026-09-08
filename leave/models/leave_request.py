from django.core.exceptions import ValidationError
from django.db import models

from base.models.company_base_model import CompanyBaseModel
from employee.models.employee import Employee
from leave.constants import LeaveRequestStatus
from leave.models.leave_type import LeaveType


class LeaveRequest(CompanyBaseModel):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="leave_requests",
    )

    leave_type = models.ForeignKey(
        LeaveType,
        on_delete=models.PROTECT,
        related_name="leave_requests",
    )

    start_date = models.DateField()

    end_date = models.DateField()

    reason = models.TextField(
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=LeaveRequestStatus.choices,
        default=LeaveRequestStatus.PENDING,
        db_index=True,
    )

    class Meta:
        ordering = ["-start_date"]

    def clean(self):
        errors = {}

        if self.end_date < self.start_date:
            errors["end_date"] = "End date must be greater than or equal to start date."

        if self.employee_id and self.employee.company_id != self.company_id:
            errors["employee"] = "Employee must belong to the same company."

        if self.leave_type_id and self.leave_type.company_id != self.company_id:
            errors["leave_type"] = "Leave type must belong to the same company."

        if errors:
            raise ValidationError(errors)
