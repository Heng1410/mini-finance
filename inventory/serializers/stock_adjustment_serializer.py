from rest_framework import serializers

from base.serializers.base_serializer import BaseSerializer
from inventory.models.stock_movement import StockMovement


class StockAdjustmentSerializer(BaseSerializer):
    actual_quantity = serializers.IntegerField(min_value=0)

    class Meta:
        model = StockMovement
        fields = ("product", "actual_quantity", "reference", "note")
