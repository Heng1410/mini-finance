from django.db import models

from base.models.company_base_model import CompanyBaseModel
from employee.models.employee import Employee
from transport.models.transport import Transport


class TransportPassenger(CompanyBaseModel):
    transport = models.ForeignKey(
        Transport, on_delete=models.CASCADE, related_name="passenger_records"
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="transport_passenger_records",
    )

    boarded_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    dropped_off_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "transport_passenger"
        constraints = [
            models.UniqueConstraint(
                fields=["transport", "employee"],
                name="unique_transport_passenger",
            ),
        ]
