from django.db import models

from base.models.company_base_model import CompanyBaseModel


# Create your models here.
class Sequence(CompanyBaseModel):
    key = models.CharField(max_length=64)
    prefix = models.CharField(max_length=8, blank=True)
    last_number = models.BigIntegerField(default=0)

    class Meta:
        db_table = "sequences"
        constraints = [
            models.UniqueConstraint(
                fields=["company", "key"], name="uq_seq_key_per_company"
            )
        ]
