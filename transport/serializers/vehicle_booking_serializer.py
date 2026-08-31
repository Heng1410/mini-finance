from rest_framework import serializers
from django.utils import timezone

from base.serializers.base_serializer import BaseSerializer
from transport.models.vehicle_booking import VehicleBooking
from transport.serializers.vehicle_serializer import VehicleSimpleSerializer
from employee.serializers.employee_serializer import EmployeeSimpleSerializer


class VehicleBookingSerializer(BaseSerializer):
    status = serializers.CharField(
        read_only=True,
    )

    class Meta:
        model = VehicleBooking
        fields = [
            "id",
            "vehicle",
            "requester",
            "purpose",
            "start_at",
            "end_at",
            "status",
            "note",
        ]

    def validate(self, attrs):
        start_at = attrs.get("start_at", getattr(self.instance, "start_at", None))
        end_at = attrs.get("end_at", getattr(self.instance, "end_at", None))

        if start_at and end_at:
            if end_at <= start_at:
                raise serializers.ValidationError(
                    {"end_at": "End time must be after start time."}
                )

        if start_at:
            if start_at < timezone.now():
                raise serializers.ValidationError(
                    {"start_at": "Booking cannot start in the past."}
                )

        return attrs


class VehicleBookingListSerializer(BaseSerializer):
    vehicle = VehicleSimpleSerializer(read_only=True)
    requester = EmployeeSimpleSerializer(read_only=True)

    class Meta:
        model = VehicleBooking
        fields = [
            "id",
            "vehicle",
            "requester",
            "purpose",
            "start_at",
            "end_at",
            "status",
        ]


class VehicleBookingDetailSerializer(VehicleBookingSerializer):
    vehicle = VehicleSimpleSerializer(read_only=True)
    requester = EmployeeSimpleSerializer(read_only=True)
