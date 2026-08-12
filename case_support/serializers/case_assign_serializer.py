from rest_framework import serializers

from base.serializers.base_serializer import BaseSerializer
from employee.models.employee import Employee


class CaseAssignSerializer(serializers.Serializer):
    employee  = serializers.PrimaryKeyRelatedField(
        queryset = Employee.objects.all()
    )