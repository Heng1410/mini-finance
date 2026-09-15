from django.db import models
from django.core.exceptions import ValidationError

from base.models.company_base_model import CompanyBaseModel
from employee.models.employee import Employee
from employee_document.constants import EmployeeDocumentType


class EmployeeDocument(CompanyBaseModel):
    employee = models.ForeignKey(
        Employee, on_delete=models.PROTECT, related_name="documents"
    )
    name = models.CharField(max_length=255)
    document_type = models.CharField(
        max_length=30,
        choices=EmployeeDocumentType.choices,
    )
    file = models.FileField(
        upload_to="employee_documents/",
    )
    issued_date = models.DateField(
        null=True,
        blank=True,
    )
    expiry_date = models.DateField(
        null=True,
        blank=True,
    )
    description = models.CharField(
        max_length=255,
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def clean(self):
        if (
            self.issued_date
            and self.expiry_date
            and self.expiry_date < self.issued_date
        ):
            raise ValidationError(
                {
                    "expiry_date": (
                        "Expiry date must be later than or equal to issued date."
                    )
                }
            )
