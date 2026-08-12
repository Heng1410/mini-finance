from base.serializers.base_serializer import BaseSerializer
from employee.serializers.employee_serializer import (
    EmployeeSimpleSerializer,
)
from inventory.models.stock_movement import StockMovement
from inventory.serializers.product_serializer import ProductListSerializer


class StockMovementSerializer(BaseSerializer):
    class Meta:
        model = StockMovement
        fields = (
            "id",
            "product",
            "movement_type",
            "quantity",
            "performed_by",
            "reference",
            "note",
        )
        read_only_fields = (
            "id",
            "performed_by",
        )


class StockMovementListSerializer(BaseSerializer):
    product = ProductListSerializer(read_only=True)
    performed_by = EmployeeSimpleSerializer(read_only=True)

    class Meta:
        model = StockMovement
        fields = (
            "id",
            "product",
            "movement_type",
            "quantity",
            "performed_by",
        )


class StockMovementDetailSerializer(StockMovementSerializer):
    product = ProductListSerializer(read_only=True)
    performed_by = EmployeeSimpleSerializer(read_only=True)
