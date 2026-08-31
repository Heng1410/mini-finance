from rest_framework import serializers

from django.db import transaction

from transport.constants import BookingStatus, VehicleStatus
from transport.models.vehicle import Vehicle
from transport.models.vehicle_booking import VehicleBooking


class VehicleBookingService:

    @staticmethod
    @transaction.atomic
    def create_booking(
        *,
        company,
        vehicle,
        requester,
        purpose,
        start_at,
        end_at,
        note=None,
    ):
        vehicle = Vehicle.objects.select_for_update().get(
            pk=vehicle.pk, company=company
        )

        if vehicle.status != VehicleStatus.ACTIVE:
            raise serializers.ValidationError("Only active vehicles can be booked.")

        conflicts = VehicleBooking.objects.filter(
            vehicle=vehicle, start_at__lt=end_at, end_at__gt=start_at
        )

        if conflicts.exists():
            raise serializers.ValidationError(
                "This vehicle is already booked during the selected time."
            )

        booking = VehicleBooking.objects.create(
            vehicle=vehicle,
            requester=requester,
            purpose=purpose,
            start_at=start_at,
            end_at=end_at,
            note=note,
            company=company,
        )

        return booking

    @staticmethod
    @transaction.atomic
    def approve_booking(*, company, booking):

        booking = VehicleBooking.objects.select_for_update().get(
            pk=booking.pk, company=company
        )

        if booking.status != BookingStatus.PENDING:
            raise serializers.ValidationError("Only pending booking can be approve.")
        
