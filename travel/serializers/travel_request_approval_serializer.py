from base.serializers.base_serializer import BaseSerializer
from employee.serializers.employee_serializer import EmployeeSimpleSerializer
from travel.models.travel_request_approval import TravelRequestApproval
from travel.serializers.travel_request_serializer import TravelRequestSimpleSerializer


class TravelRequestApprovalSerializer(BaseSerializer):
    class Meta:
        model = TravelRequestApproval
        fields = ("id", "travel_request", "approved_by", "approved_at", "remarks")
        read_only_fields = ("id", "travel_request", "approved_by", "approved_at")


class TravelRequestApprovalListSerializer(BaseSerializer):
    travel_request = TravelRequestSimpleSerializer(read_only=True)
    approved_by = EmployeeSimpleSerializer(read_only=True)

    class Meta:
        model = TravelRequestApproval
        fields = ("id", "travel_request", "approved_by", "approved_at", "remarks")


class TravelRequestApprovalDetailSerializer(TravelRequestApprovalSerializer):
    travel_request = TravelRequestSimpleSerializer(read_only=True)
    approved_by = EmployeeSimpleSerializer(read_only=True)
