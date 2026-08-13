from base.serializers.base_serializer import BaseSerializer
from case_support.models.case_activity import CaseActivity
from employee.serializers.employee_serializer import EmployeeSimpleSerializer


class CaseActivitySerializer(BaseSerializer):
    created_by = EmployeeSimpleSerializer(read_only=True)

    class Meta:
        model = CaseActivity
        fields = ("id", "activity_type", "message", "created_by", "created_at")
        read_only_fields = ("id", "activity_type", "created_by", "created_at")
