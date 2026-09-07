from base.serializers.base_serializer import BaseSerializer
from delivery.models.delivery import Delivery
from sales_order.serializers.sales_order_serializer import SalesOrderSerializer


class DeliverySerializer(BaseSerializer):
    class Meta:
        model = Delivery
        fields = (
            "id",
            "delivery_number",
            "sales_order",
            "status",
            "delivery_date",
            "created_by",
            "confirmed_by",
            "confirmed_at",
            "notes",
        )
        read_only_fields = (
            "id",
            "delivery_number",
            "status",
            "created_by",
            "confirmed_by",
            "confirmed_at",
        )

    def validate(self, attrs):
        return attrs


class DeliveryListSerializer(BaseSerializer):
    sales_order = SalesOrderSerializer(read_only=True)

    class Meta:
        model = Delivery
        fields = ("id", "delivery_number", "sales_order", "status", "delivery_date")


class DeliveryDetailSerializer(DeliverySerializer):
    sales_order = SalesOrderSerializer(read_only=True)
