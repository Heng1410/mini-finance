from rest_framework import serializers

from django.utils import timezone

from base.serializers.base_serializer import BaseSerializer
from transport.models.vehicle_maintenance import VehicleMaintenance
from transport.serializers.vehicle_serializer import VehicleSimpleSerializer


class VehicleMaintenanceSerializer(BaseSerializer):
    class Meta:
        model = VehicleMaintenance
        fields = [
            "id",
            "vehicle",
            "maintenance_type",
            "maintenance_date",
            "cost",
            "mileage",
            "description",
        ]

    def validate_cost(self, value):
        if value < 0:
            raise serializers.ValidationError("Maintenance cost cannot be negative.")
        return value

    def validate_maintenance_date(self, value):
        if value > timezone.localdate():
            raise serializers.ValidationError(
                "Maintenance date cannot be in the future."
            )
        return value

    def validate(self, attrs):
        vehicle = attrs.get("vehicle")
        maintenance_type = attrs.get("maintenance_type")
        maintenance_date = attrs.get("maintenance_date")
        mileage = attrs.get("mileage")

        queryset = VehicleMaintenance.objects.filter(
            vehicle=vehicle,
            maintenance_type=maintenance_type,
            maintenance_date=maintenance_date,
            mileage=mileage,
        )

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "This maintenance record already exists for this vehicle."
            )

        return attrs


class VehicleListMaintenanceSerializer(BaseSerializer):
    vehicle = VehicleSimpleSerializer(read_only=True)

    class Meta:
        model = VehicleMaintenance
        fields = [
            "id",
            "vehicle",
            "maintenance_type",
            "maintenance_date",
            "cost",
            "mileage",
            "description",
        ]


class VehicleDetailMaintenanceSerializer(VehicleMaintenanceSerializer):
    vehicle = VehicleSimpleSerializer(read_only=True)
