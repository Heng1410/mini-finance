from django.db import models

from base.models.base_model import BaseModel
from company.models.company import Company


class CompanyBaseModel(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, editable=False)

    class Meta:
        abstract = True
