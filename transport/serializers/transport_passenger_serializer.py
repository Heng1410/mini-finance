from rest_framework import serializers

from base.serializers.base_serializer import BaseSerializer
from employee.serializers.employee_serializer import EmployeeSimpleSerializer
from transport.models.transport_passenger import TransportPassenger
from transport.serializers.transport_serializer import TransportSimpleSerializer


class TransportPassengerSerializer(BaseSerializer):
    class Meta:
        model = TransportPassenger
        fields = [
            "id",
            "transport",
            "employee",
            "boarded_at",
            "dropped_off_at",
        ]

    def validate(self, attrs):
        boarded_at = attrs.get("boarded_at", getattr(self.instance, "boarded_at", None))

        dropped_off_at = attrs.get(
            "dropped_off_at", getattr(self.instance, "dropped_off_at", None)
        )

        if boarded_at and dropped_off_at and dropped_off_at < boarded_at:
            raise serializers.ValidationError(
                {
                    "dropped_off_at": (
                        "Drop-off time cannot be earlier than boarding time."
                    )
                }
            )

        transport = attrs.get(
            "transport",
            getattr(self.instance, "transport", None),
        )

        employee = attrs.get(
            "employee",
            getattr(self.instance, "employee", None),
        )

        if transport and employee:
            if transport.driver_id == employee.id:
                raise serializers.ValidationError(
                    {"employee": "The driver cannot also be a passenger."}
                )

        return attrs


class TransportPassengerListSerializer(BaseSerializer):
    transport = TransportSimpleSerializer(read_only=True)
    employee = EmployeeSimpleSerializer(read_only=True)

    class Meta:
        model = TransportPassenger
        fields = [
            "id",
            "transport",
            "employee",
            "boarded_at",
            "dropped_off_at",
        ]


class TransportPassengerDetailSerializer(TransportPassengerSerializer):
    transport = TransportSimpleSerializer(read_only=True)
    employee = EmployeeSimpleSerializer(read_only=True)
