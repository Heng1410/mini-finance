from base.serializers.base_serializer import BaseSerializer
from inventory.serializers.product_serializer import ProductListSerializer
from purchase_order.models.purchase_order_item import PurchaseOrderItem
from purchase_order.serializers.purchase_order_serializer import (
    PurchaseOrderListSerializer,
)


class PurchaseOrderItemSerializer(BaseSerializer):
    class Meta:
        model = PurchaseOrderItem
        fields = (
            "id",
            "purchase_order",
            "product",
            "quantity",
            "unit_price",
            "sub_total",
        )
        read_only_fields = ("id", "sub_total")


class PurchaseOrderItemListSerializer(BaseSerializer):
    purchase_order = PurchaseOrderListSerializer(read_only=True)
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = PurchaseOrderItem
        fields = (
            "id",
            "purchase_order",
            "product",
            "quantity",
            "unit_price",
            "sub_total",
        )


class PurchaseOrderItemDetailSerializer(PurchaseOrderItemSerializer):
    purchase_order = PurchaseOrderListSerializer(read_only=True)
    product = ProductListSerializer(read_only=True)
