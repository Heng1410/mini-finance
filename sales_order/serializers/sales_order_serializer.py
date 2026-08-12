from accounts_receivable.serializers.customer_serializer import CustomerListSerializer
from base.serializers.base_serializer import BaseSerializer
from sales_order.models.sales_order import SalesOrder


class SalesOrderSerializer(BaseSerializer):
    class Meta:
        model = SalesOrder
        fields = (
            "id",
            "order_number",
            "customer",
            "status",
            "total_amount",
            "created_by",
        )
        read_only_fields = (
            "id",
            "order_number",
            "status",
            "total_amount",
            "created_by",
        )


class SalesOrderListSerializer(BaseSerializer):
    customer = CustomerListSerializer(read_only=True)

    class Meta:
        model = SalesOrder
        fields = (
            "id",
            "order_number",
            "customer",
            "status",
            "total_amount",
            "created_by",
        )


class SalesOrderDetailSerializer(SalesOrderSerializer):
    customer = CustomerListSerializer(read_only=True)
