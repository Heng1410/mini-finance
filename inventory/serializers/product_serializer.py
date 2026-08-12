from base.serializers.base_serializer import BaseSerializer
from inventory.models.products import Product

from rest_framework import serializers


class ProductSerializer(BaseSerializer):
    stock_quantity = serializers.IntegerField(min_value=0)

    class Meta:
        model = Product
        fields = ("id", "sku", "name", "stock_quantity", "is_active")

        def validate_sku(self, value):
            return value.strip().upper()


class ProductListSerializer(BaseSerializer):
    class Meta:
        model = Product
        fields = ("id", "sku", "name", "stock_quantity", "is_active")


class ProductDetailSerializer(ProductSerializer):
    pass
