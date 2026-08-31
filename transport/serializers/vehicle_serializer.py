from rest_framework import serializers

from base.serializers.base_serializer import BaseSerializer
from employee.serializers.employee_serializer import EmployeeSimpleSerializer
from transport.models.vehicle import Vehicle


class VehicleSerializer(BaseSerializer):
    class Meta:
        model = Vehicle
        fields = [
            "id",
            "plate_number",
            "vehicle_type",
            "brand",
            "model",
            "year",
            "vin",
            "status",
            "driver",
            "purchase_date",
            "note",
        ]

    def validate_plate_number(self, value):
        value = value.strip().upper()  # Normalize the plate number

        if not value:
            raise serializers.ValidationError("Plate number is required.")
        return value

    def validate_vin(self, value):
        if not value:
            return value  # Allow empty VIN

        value = value.strip().upper()  # Normalize the VIN

        if len(value) != 17:
            raise serializers.ValidationError("VIN must be exactly 17 characters long.")

        if any(char in value for char in "IOQ"):
            raise serializers.ValidationError(
                "VIN cannot contain the letters I, O, or Q."
            )

        return value

    def validate(self, attrs):
        year = attrs.get("year", getattr(self.instance, "year", None))
        purchase_date = attrs.get(
            "purchase_date", getattr(self.instance, "purchase_date", None)
        )

        if year and purchase_date:
            if purchase_date.year < year:
                raise serializers.ValidationError(
                    {
                        "purchase_date": (
                            "Purchase date cannot be earlier "
                            "than the vehicle's manufacturing year."
                        )
                    }
                )

        return attrs


class VehicleListSerializer(BaseSerializer):
    driver = EmployeeSimpleSerializer(read_only=True)

    class Meta:
        model = Vehicle
        fields = [
            "id",
            "plate_number",
            "vehicle_type",
            "brand",
            "model",
            "year",
            "vin",
            "status",
            "driver",
            "purchase_date",
            "note",
        ]


class VehicleSimpleSerializer(BaseSerializer):
    class Meta:
        model = Vehicle
        fields = ["id", "brand", "model", "vehicle_type"]


class VehicleDetailSerializer(VehicleSerializer):
    driver = EmployeeSimpleSerializer(read_only=True)
