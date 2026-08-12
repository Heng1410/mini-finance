from base.serializers.base_serializer import BaseSerializer
from inventory.serializers.product_serializer import ProductListSerializer
from sales_order.models.sales_order_item import SalesOrderItem
from sales_order.serializers.sales_order_serializer import SalesOrderListSerializer


class SalesOrderItemSerializer(BaseSerializer):
    class Meta:
        model = SalesOrderItem
        fields = ("id", "sales_order", "product", "quantity", "unit_price", "sub_total")
        read_only_fields = ("id", "sub_total")


class SalesOrderItemListSerializer(BaseSerializer):
    sales_order = SalesOrderListSerializer(read_only=True)
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = SalesOrderItem
        fields = ("id", "sales_order", "product", "quantity")


class SalesOrderItemDetailSerializer(SalesOrderItemSerializer):
    sales_order = SalesOrderListSerializer(read_only=True)
    product = ProductListSerializer(read_only=True)
