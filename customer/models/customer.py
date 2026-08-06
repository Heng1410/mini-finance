from django.db import models

from base.models.company_base_model import CompanyBaseModel


# Create your models here.
class Customer(CompanyBaseModel):
    code = models.CharField(max_length=32)
    name = models.CharField(max_length=255)
    phone = models.CharField()