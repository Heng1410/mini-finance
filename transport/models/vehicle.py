from django.db import models

from base.models.company_base_model import CompanyBaseModel
from employee.models.employee import Employee
from transport.constants import VehicleStatus, VehicleType


class Vehicle(CompanyBaseModel):
    plate_number = models.CharField(max_length=20)
    vehicle_type = models.CharField(
        max_length=20,
        choices=VehicleType.choices,
    )
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    year = models.PositiveIntegerField()

    vin = models.CharField(
        max_length=17,
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=20,
        choices=VehicleStatus.choices,
    )
    driver = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        related_name="assigned_vehicles",
        null=True,
        blank=True,
    )

    purchase_date = models.DateField(null=True, blank=True)

    note = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "vehicle"
        constraints = [
            models.UniqueConstraint(
                fields=["company", "plate_number"],
                name="unique_vehicle_plate_per_company",
            ),
            models.UniqueConstraint(
                fields=["company", "vin"],
                name="unique_vehicle_vin_per_company",
            ),
        ]
