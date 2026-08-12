from django.utils import timezone

from rest_framework import serializers

from base.serializers.base_serializer import BaseSerializer
from inventory.models.stock_reservation import StockReservation
from inventory.serializers.product_serializer import ProductListSerializer


class StockReservationSerializer(BaseSerializer):
    class Meta:
        model = StockReservation
        fields = (
            "id",
            "product",
            "quantity",
            "status",
            "reserved_by",
            "reserved_at",
            "expires_at",
        )
        read_only_fields = (
            "id",
            "status",
            "reserved_by",
            "reserved_at",
        )

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value

    def validate_expires_at(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("Expiration time must be in the future.")
        return value


class StockReservationListSerializer(BaseSerializer):
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = StockReservation
        fields = (
            "id",
            "product",
            "quantity",
            "status",
            "reserved_by",
            "reserved_at",
            "expires_at",
        )


class StockReservationDetailSerializer(StockReservationSerializer):
    product = ProductListSerializer(read_only=True)
