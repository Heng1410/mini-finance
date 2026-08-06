from django.db import models

from base.models.base_model import BaseModel


# Create your models here.
class Company(BaseModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=16, unique=True)
    legal_name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=16, unique=True)
    tax_number = models.CharField(max_length=20, unique=True)

    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)

    address_line_1 = models.CharField(max_length=255, null=True, blank=True)
    address_line_2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255)

    currency = models.CharField(max_length=16)
    timezone = models.CharField(max_length=32)
    fiscal_year_start = models.DateField()

    logo = models.ImageField(null=True, blank=True)

    description = models.TextField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
