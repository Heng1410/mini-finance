from django.db import models

from base.models.company_base_model import CompanyBaseModel
from employee.models.employee import Employee
from transport.constants import BookingStatus
from transport.models.vehicle import Vehicle


class VehicleBooking(CompanyBaseModel):
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.PROTECT,
        related_name="bookings",
    )

    requester = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="vehicle_bookings",
    )

    purpose = models.CharField(
        max_length=255,
    )

    start_at = models.DateTimeField()

    end_at = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.PENDING,
    )

    note = models.TextField(
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "vehicle_booking"