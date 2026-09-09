from django.core.exceptions import ValidationError
from django.db import models

from base.models.company_base_model import CompanyBaseModel


class WorkSchedule(CompanyBaseModel):
    name = models.CharField(
        max_length=100,
    )

    start_time = models.TimeField()

    end_time = models.TimeField()

    working_days = models.JSONField(
        default=list,
        help_text="List of working days, e.g. [1, 2, 3, 4, 5] where Monday=1.",
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    class Meta:
        ordering = ["name"]

        constraints = [
            models.UniqueConstraint(
                fields=["company", "name"],
                name="unique_work_schedule_name_per_company",
            ),
        ]

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError(
                {
                    "end_time": (
                        "End time must be later than start time."
                    )
                }
            )

        if not isinstance(self.working_days, list):
            raise ValidationError(
                {
                    "working_days": (
                        "Working days must be a list."
                    )
                }
            )

        if not all(
            isinstance(day, int) and 1 <= day <= 7
            for day in self.working_days
        ):
            raise ValidationError(
                {
                    "working_days": (
                        "Working days must contain integers from 1 to 7."
                    )
                }
            )