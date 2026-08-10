from base.serializers.base_serializer import BaseSerializer
from sequence.models.sequence import Sequence


class SequenceSerializer(BaseSerializer):
    class Meta:
        model = Sequence
        fields = ("id", "key", "prefix", "last_number")
        read_only_fields = ("last_number",)
