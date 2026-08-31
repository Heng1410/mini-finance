from rest_framework import serializers
from decimal import Decimal, ROUND_HALF_UP

from base.serializers.base_serializer import BaseSerializer
from transport.models.fuel_transaction import FuelTransaction
from transport.serializers.vehicle_serializer import VehicleSimpleSerializer


class FuelTransactionSerializer(BaseSerializer):
    total_cost = serializers.DecimalField(
        max_digits=15, decimal_places=2, read_only=True
    )

    class Meta:
        model = FuelTransaction
        fields = [
            "id",
            "vehicle",
            "fuel_date",
            "fuel_type",
            "quantity",
            "price_per_unit",
            "total_cost",
            "mileage",
            "station",
            "reference",
            "note",
        ]

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")

        return value

    def validate_price_per_unit(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Price per unit must be greater than zero."
            )

        return value

    def create(self, validated_data):
        validated_data["total_cost"] = self._calculate_total(
            validated_data["quantity"],
            validated_data["price_per_unit"],
        )

        return super().create(validated_data)

    def update(self, instance, validated_data):
        quantity = validated_data.get(
            "quantity",
            instance.quantity,
        )

        price_per_unit = validated_data.get(
            "price_per_unit",
            instance.price_per_unit,
        )

        validated_data["total_cost"] = self._calculate_total(
            quantity,
            price_per_unit,
        )

        return super().update(instance, validated_data)

    @staticmethod
    def _calculate_total(quantity, price_per_unit):
        return (quantity * price_per_unit).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )


class FuelTransactionListSerializer(BaseSerializer):
    vehicle = VehicleSimpleSerializer(read_only=True)

    class Meta:
        model = FuelTransaction
        fields = [
            "id",
            "vehicle",
            "fuel_date",
            "fuel_type",
            "quantity",
            "price_per_unit",
            "total_cost",
            "mileage",
            "station",
        ]


class FuelTransactionDetailSerializer(FuelTransactionSerializer):
    vehicle = VehicleSimpleSerializer(read_only=True)
