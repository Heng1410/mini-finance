from base.models.company_base_model import CompanyBaseModel
from django.db import models

from employee.models.employee import Employee


class Notification(CompanyBaseModel):
    recipient = models.ForeignKey(
        Employee, on_delete=models.PROTECT, related_name="notifications"
    )

    title = models.CharField(max_length=255)

    message = models.TextField()

    is_read = models.BooleanField(default=False)

    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "notifications"
