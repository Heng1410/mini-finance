from rest_framework import serializers

from base.serializers.base_serializer import BaseSerializer
from employee.serializers.employee_serializer import EmployeeSimpleSerializer
from transport.models.transport import Transport
from transport.serializers.vehicle_serializer import VehicleSimpleSerializer


class TransportSerializer(BaseSerializer):
    class Meta:
        model = Transport
        fields = [
            "id",
            "vehicle",
            "driver",
            "origin",
            "destination",
            "departure_at",
            "arrival_at",
            "distance",
            "transport_type",
            "status",
            "note",
        ]

    def validate_distance(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Distance cannot be negative.")
        return value

    def validate(self, attrs):
        departure_at = attrs.get(
            "departure_at", getattr(self.instance, "departure_at", None)
        )

        arrival_at = attrs.get("arrival_at", getattr(self.instance, "arrival_at", None))

        if arrival_at and arrival_at < departure_at:
            raise serializers.ValidationError(
                {
                    "arrival_at": (
                        "Arrival time cannot be earlier " "than departure time."
                    )
                }
            )

        return attrs


class TransportListSerializer(BaseSerializer):
    vehicle = VehicleSimpleSerializer(read_only=True)
    driver = EmployeeSimpleSerializer(read_only=True)

    class Meta:
        model = Transport
        fields = [
            "id",
            "vehicle",
            "driver",
            "origin",
            "destination",
            "departure_at",
            "arrival_at",
            "distance",
            "status",
        ]


class TransportSimpleSerializer(BaseSerializer):
    vehicle = VehicleSimpleSerializer(read_only=True)
    driver = EmployeeSimpleSerializer(read_only=True)

    class Meta:
        model = Transport
        fields = [
            "vehicle",
            "driver",
            "departure_at",
            "arrival_at",
            "distance",
        ]


class TransportDetailSerializer(TransportSerializer):
    vehicle = VehicleSimpleSerializer(read_only=True)
    driver = EmployeeSimpleSerializer(read_only=True)
