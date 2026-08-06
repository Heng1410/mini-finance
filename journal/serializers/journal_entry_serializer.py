from django.db import transaction
from rest_framework import serializers

from base.serializers.base_serializer import BaseSerializer
from journal.constants import JournalStatus
from journal.models.journal_entry import JournalEntry
from journal.models.journal_entry_line import JournalEntryLine
from journal.serializers.journal_entry_line_serializer import JournalEntryLineSerializer


class JournalEntrySerializer(BaseSerializer):
    lines = JournalEntryLineSerializer(many=True)

    class Meta:
        model = JournalEntry
        fields = ("id", "journal_no", "date", "description", "status", "lines")

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        lines = validated_data.get("lines", [])
        total_debit = 0
        total_credit = 0
        total_lines = len(lines)

        if self.instance and self.instance.status == JournalStatus.POSTED:
            raise serializers.ValidationError(
                {"details": ["Posted journals cannot be modified."]}
            )

        if total_lines < 2:
            raise serializers.ValidationError(
                {"lines": ["A journal entry must contain at least two lines."]}
            )

        for line in lines:
            debit = line.get("debit")
            credit = line.get("credit")

            total_debit += debit
            total_credit += credit

        if total_debit != total_credit:
            raise serializers.ValidationError(
                {"lines": ["Total debit must equal total credit."]}
            )

        return validated_data

    @transaction.atomic
    def create(self, validated_data):
        lines = validated_data.pop("lines")

        journal = JournalEntry.objects.create(**validated_data)
        for line in lines:
            JournalEntryLine.objects.create(journal=journal, **line)

        return journal


class JournalEntryListSerializer(BaseSerializer):

    class Meta:
        model = JournalEntry
        fields = ("id", "journal_no", "date", "description", "status")


class JournalEntryDetailSerializer(BaseSerializer):
    lines = JournalEntryLineSerializer(many=True, read_only=True)

    class Meta:
        model = JournalEntry
        fields = ("id", "journal_no", "date", "description", "status", "lines")
