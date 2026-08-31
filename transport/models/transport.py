from django.db import models

from base.models.company_base_model import CompanyBaseModel
from employee.models.employee import Employee
from transport.constants import TransportStatus, TransportType
from transport.models.vehicle import Vehicle


class Transport(CompanyBaseModel):
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.PROTECT,
        related_name="transport_trips",
    )

    driver = models.ForeignKey(
        Employee, on_delete=models.PROTECT, related_name="transport_trips"
    )

    passengers = models.ManyToManyField(
        Employee,
        through="TransportPassenger",
        related_name="passenger_transports",
        blank=True,
    )

    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)

    departure_at = models.DateTimeField()
    arrival_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    distance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    transport_type = models.CharField(
        max_length=30,
        choices=TransportType.choices,
    )

    status = models.CharField(
        max_length=30,
        choices=TransportStatus.choices,
    )

    note = models.TextField(
        blank=True,
        null=True,
    )
