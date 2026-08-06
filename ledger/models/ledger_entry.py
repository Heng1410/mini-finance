from django.db import models

from account.models.account import Account
from base.models.company_base_model import CompanyBaseModel
from journal.models.journal_entry import JournalEntry
from journal.models.journal_entry_line import JournalEntryLine


# Create your models here.
class LedgerEntry(CompanyBaseModel):
    journal = models.ForeignKey(
        JournalEntry, on_delete=models.PROTECT, related_name="ledger_entries"
    )
    journal_line = models.ForeignKey(
        JournalEntryLine, on_delete=models.CASCADE, related_name="ledger_entries"
    )
    account = models.ForeignKey(
        Account, on_delete=models.PROTECT, related_name="ledger_entries"
    )
    date = models.DateField()
    description = models.TextField(null=True, blank=True)

    debit = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    class Meta:
        db_table = "ledger_entry"
