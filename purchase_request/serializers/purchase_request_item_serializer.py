from base.serializers.base_serializer import BaseSerializer
from inventory.serializers.product_serializer import ProductListSerializer
from purchase_request.models.purchase_request_item import PurchaseRequestItem
from purchase_request.serializers.purchase_request_serializer import (
    PurchaseRequestListSerializer,
)


class PurchaseRequestItemSerializer(BaseSerializer):
    class Meta:
        model = PurchaseRequestItem
        fields = (
            "id",
            "purchase_request",
            "product",
            "quantity",
            "estimated_unit_price",
            "estimated_subtotal",
        )
        read_only_fields = ("id", "estimated_subtotal")


class PurchaseRequestItemListSerializer(BaseSerializer):
    purchase_request = PurchaseRequestListSerializer(read_only=True)
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = PurchaseRequestItem
        fields = (
            "id",
            "purchase_request",
            "product",
            "quantity",
            "estimated_unit_price",
            "estimated_subtotal",
        )


class PurchaseRequestItemDetailSerializer(PurchaseRequestItemSerializer):
    purchase_request = PurchaseRequestListSerializer(read_only=True)
    product = ProductListSerializer(read_only=True)
    
