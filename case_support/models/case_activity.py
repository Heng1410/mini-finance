from django.db import models

from base.models.company_base_model import CompanyBaseModel
from case_support.constants import CaseActivityType
from case_support.models.case import Case
from employee.models.employee import Employee


class CaseActivity(CompanyBaseModel):
    case = models.ForeignKey(Case, on_delete=models.PROTECT, related_name="activities")

    activity_type = models.CharField(
        max_length=30,
        choices=CaseActivityType.choices,
    )

    message = models.TextField()

    created_by = models.ForeignKey(
        Employee, on_delete=models.PROTECT, related_name="case_activities"
    )

    class Meta:
        db_table = "case_activities"
