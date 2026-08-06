from django.db import transaction
from rest_framework import serializers

from journal.constants import JournalStatus
from ledger.models.ledger_entry import LedgerEntry


class PostJournalSerializer(serializers.Serializer):

    def validate(self, attrs):
        journal = self.context["journal"]
        if journal.status != JournalStatus.DRAFT:
            raise serializers.ValidationError(
                {"details": ["Only draft journals can be posted."]}
            )
        return attrs

    @transaction.atomic
    def save(self, **kwargs):
        journal = self.context["journal"]

        for line in journal.lines.all():
            LedgerEntry.objects.create(
                journal=journal,
                journal_line=line,
                account=line.account,
                date=journal.date,
                description=line.description,
                debit=line.debit,
                credit=line.credit,
                company=journal.company
            )

        journal.status = JournalStatus.POSTED
        journal.save(update_fields=["status"])

        return journal
