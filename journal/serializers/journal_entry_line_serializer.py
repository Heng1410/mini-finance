from rest_framework import serializers

from account.models.account import Account
from base.serializers.base_serializer import BaseSerializer
from journal.models.journal_entry_line import JournalEntryLine


class JournalEntryLineSerializer(BaseSerializer):
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())

    class Meta:
        model = JournalEntryLine
        fields = ("id", "account", "description", "debit", "credit")
