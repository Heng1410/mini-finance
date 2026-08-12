from rest_framework import serializers


class CaseResolveSerializer(serializers.Serializer):
    resolution_note = serializers.CharField(
        max_length=255, allow_null=True, allow_blank=True
    )
