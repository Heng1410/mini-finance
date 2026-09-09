from django.core.exceptions import ValidationError
from django.db import models

from attendance.constants import AttendanceStatus
from base.models.company_base_model import CompanyBaseModel
from employee.models.employee import Employee


class Attendance(CompanyBaseModel):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="attendances",
    )

    date = models.DateField()

    check_in = models.TimeField(
        null=True,
        blank=True,
    )

    check_out = models.TimeField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=AttendanceStatus.choices,
        default=AttendanceStatus.PRESENT,
        db_index=True,
    )

    note = models.CharField(
        max_length=255,
        blank=True,
    )

    class Meta:
        ordering = ["-date"]
        constraints = [
            models.UniqueConstraint(
                fields=["company", "employee", "date"],
                name="unique_attendance_per_employee_day",
            ),
        ]

    def clean(self):
        if self.check_in and self.check_out:
            if self.check_out <= self.check_in:
                raise ValidationError(
                    {"check_out": ("Check-out time must be later than check-in time.")}
                )
