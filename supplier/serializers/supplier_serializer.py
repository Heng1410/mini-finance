from base.serializers.base_serializer import BaseSerializer
from supplier.models.supplier import Supplier


class SupplierSerializer(BaseSerializer):
    class Meta:
        model = Supplier
        fields = ("id", "code", "name", "phone", "email", "address", "is_active")
        read_only_fields = ("id",)


class SupplierListSerializer(BaseSerializer):
    class Meta:
        model = Supplier
        fields = ("id", "code", "name", "phone", "email", "is_active")
        
class SupplierDetailSerializer(SupplierSerializer):
    pass
