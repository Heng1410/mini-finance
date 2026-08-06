from django.db import models

from account.models.account import Account
from journal.models.journal_entry import JournalEntry


class JournalEntryLine(models.Model):
    journal = models.ForeignKey(
        JournalEntry, on_delete=models.CASCADE, related_name="lines"
    )

    account = models.ForeignKey(
        Account, on_delete=models.PROTECT, related_name="journal_lines"
    )

    description = models.TextField(blank=True, null=True)
    debit = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    class Meta:
        db_table = "journal_entry_lines"
        ordering = ("id",)
        constraints = [
            models.CheckConstraint(
                check=(
                    (models.Q(debit__gt=0) & models.Q(credit=0))
                    | (models.Q(credit__gt=0) & models.Q(debit=0))
                ),
                name="chk_debit_or_credit",
            ),
        ]
