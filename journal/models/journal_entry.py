from django.db import models

from base.models.company_base_model import CompanyBaseModel
from journal.constants import JournalStatus


# Create your models here.
class JournalEntry(CompanyBaseModel):
    journal_no = models.CharField(max_length=30, db_index=True)
    date = models.DateField()
    description = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=JournalStatus.choices, default=JournalStatus.DRAFT
    )

    class Meta:
        db_table = "journal_entries"
        ordering = ("-date", "-id")
        constraints = [
            models.UniqueConstraint(
                fields=["company", "journal_no"],
                name="uq_journal_no_per_company",
            )
        ]
