from base.serializers.base_serializer import BaseSerializer
from case_support.models.case_sla import CaseSla


class CaseSlaSerializer(BaseSerializer):
    class Meta:
        model = CaseSla
        fields = (
            "id",
            "response_due_at",
            "resolution_due_at",
            "response_breached",
            "resolution_breached",
        )
        read_only_fields = (
            "id",
            "response_due_at",
            "resolution_due_at",
            "response_breached",
            "resolution_breached",
        )
