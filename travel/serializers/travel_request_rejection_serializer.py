from base.serializers.base_serializer import BaseSerializer
from employee.serializers.employee_serializer import EmployeeSimpleSerializer
from travel.models.travel_request_rejection import TravelRequestRejection
from travel.serializers.travel_request_serializer import TravelRequestSimpleSerializer


class TravelRequestRejectionSerializer(BaseSerializer):
    class Meta:
        model = TravelRequestRejection
        fields = ("id", "travel_request", "rejected_by", "rejected_at", "remarks")
        read_only_fields = (
            "id",
            "travel_request",
            "rejected_by",
            "rejected_at",
        )


class TravelRequestRejectionListSerializer(BaseSerializer):
    travel_request = TravelRequestSimpleSerializer(read_only=True)
    rejected_by = EmployeeSimpleSerializer(read_only=True)

    class Meta:
        model = TravelRequestRejection
        fields = ("id", "travel_request", "rejected_by", "rejected_at", "remarks")


class TravelRequestRejectionDetailSerializer(TravelRequestRejectionSerializer):
    travel_request = TravelRequestSimpleSerializer(read_only=True)
    rejected_by = EmployeeSimpleSerializer(read_only=True)
