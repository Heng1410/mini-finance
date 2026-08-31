from django.db import models

from base.models.company_base_model import CompanyBaseModel
from transport.constants import FuelType
from transport.models.vehicle import Vehicle


class FuelTransaction(CompanyBaseModel):
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.PROTECT,
        related_name="fuel_transactions",
    )

    fuel_date = models.DateField()

    fuel_type = models.CharField(
        max_length=20,
        choices=FuelType.choices,
    )

    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    price_per_unit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    total_cost = models.DecimalField(
        max_digits=15,
        decimal_places=2,
    )

    mileage = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    station = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    reference = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    note = models.TextField(
        blank=True,
        null=True,
    )