from django.db import models

from base.models.company_base_model import CompanyBaseModel
from transport.constants import MaintenanceType
from transport.models.vehicle import Vehicle


class VehicleMaintenance(CompanyBaseModel):
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.PROTECT, related_name="maintenance_records"
    )
    maintenance_type = models.CharField(
        max_length=30,
        choices=MaintenanceType.choices,
    )
    maintenance_date = models.DateField()
    cost = models.DecimalField(max_digits=15, decimal_places=2)
    mileage = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "vehicle_maintenance"
