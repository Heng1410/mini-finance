from rest_framework import serializers

from base.serializers.base_serializer import BaseSerializer
from employee.serializers.employee_serializer import EmployeeSimpleSerializer
from travel.models.travel_request import TravelRequest
from travel.serializers.destination_serializer import DestinationListSerializer


class TravelRequestSerializer(BaseSerializer):
    class Meta:
        model = TravelRequest
        fields = (
            "id",
            "employee",
            "destination",
            "purpose",
            "start_date",
            "end_date",
            "status",
        )
        read_only_fields = ("id", "status", "employee")

    def validate_destination(self, destination):
        company = self.context["request"].user.employee.company

        if destination.company_id != company.id:
            raise serializers.ValidationError(
                "Destination does not belong to your company."
            )

        if not destination.is_active:
            raise serializers.ValidationError("Destination is inactive.")

        return destination

    def validate(self, attrs):
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")

        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError("Start date must be before end date.")

        return attrs


class TravelRequestListSerializer(BaseSerializer):
    employee = EmployeeSimpleSerializer(read_only=True)
    destination = DestinationListSerializer(read_only=True)

    class Meta:
        model = TravelRequest
        fields = (
            "id",
            "employee",
            "destination",
            "purpose",
            "start_date",
            "end_date",
            "status",
        )


class TravelRequestDetailSerializer(TravelRequestSerializer):
    employee = EmployeeSimpleSerializer(read_only=True)
    destination = DestinationListSerializer(read_only=True)


class TravelRequestSimpleSerializer(BaseSerializer):
    destination = DestinationListSerializer(read_only=True)

    class Meta:
        model = TravelRequest
        fields = (
            "id",
            "destination",
            "purpose",
            "status",
        )
