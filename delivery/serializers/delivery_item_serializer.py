from base.serializers.base_serializer import BaseSerializer
from delivery.models.delivery_item import DeliveryItem
from inventory.serializers.product_serializer import ProductListSerializer
from sales_order.serializers.sales_order_item_serializer import (
    SalesOrderItemListSerializer,
)


class DeliveryItemSerializer(BaseSerializer):
    class Meta:
        model = DeliveryItem
        fields = (
            "id",
            "delivery",
            "sales_order_item",
            "product",
            "quantity",
            "unit_price",
            "amount",
        )
        read_only_fields = (
            "id",
            "product",
            "delivery",
            "unit_price",
            "amount",
        )


class DeliveryItemListSerializer(BaseSerializer):
    sales_order_item = SalesOrderItemListSerializer(read_only=True)
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = DeliveryItem
        fields = (
            "id",
            "sales_order_item",
            "product",
            "quantity",
            "unit_price",
            "amount",
        )


class DeliveryItemDetailSerializer(DeliveryItemSerializer):
    sales_order_item = SalesOrderItemListSerializer(read_only=True)
    product = ProductListSerializer(read_only=True)
