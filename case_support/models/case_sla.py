from django.db import models

from base.models.company_base_model import CompanyBaseModel
from case_support.models.case import Case


class CaseSla(CompanyBaseModel):

    case = models.OneToOneField(Case, on_delete=models.PROTECT, related_name="sla")

    response_due_at = models.DateTimeField()

    resolution_due_at = models.DateTimeField()

    response_breached = models.BooleanField(default=False)

    resolution_breached = models.BooleanField(default=False)

    class Meta:
        db_table = "case_slas"
