from rest_framework import serializers


class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True
        read_only_fields = ("id", "created_at", "updated_at")
