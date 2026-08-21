from django.db import models

from base.models.company_base_model import CompanyBaseModel


# Create your models here.
class Destination(CompanyBaseModel):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "destinations"
        constraints = [
            models.UniqueConstraint(
                fields=["company", "name", "country", "city"],
                name="uq_destination_company_name_country_city",
            )
        ]
