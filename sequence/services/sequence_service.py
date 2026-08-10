from django.db import transaction

from sequence.models.sequence import Sequence


class SequenceService:

    @classmethod
    @transaction.atomic
    def next(cls, *, company, key):
        sequence = Sequence.objects.select_for_update().get(company=company, key=key)
        sequence.last_number += 1
        sequence.save(update_fields=["last_number"])

        return f"{sequence.prefix}{sequence.last_number:06d}"
