from base.serializers.base_serializer import BaseSerializer
from employee.serializers.employee_serializer import EmployeeSimpleSerializer
from purchase_order.models.purchase_order import PurchaseOrder
from purchase_request.serializers.purchase_request_serializer import (
    PurchaseRequestListSerializer,
)
from supplier.serializers.supplier_serializer import SupplierListSerializer


class PurchaseOrderSerializer(BaseSerializer):
    class Meta:
        model = PurchaseOrder
        fields = (
            "id",
            "order_number",
            "purchase_request",
            "supplier",
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


class PurchaseOrderListSerializer(BaseSerializer):
    purchase_request = PurchaseRequestListSerializer(read_only=True)
    supplier = SupplierListSerializer(read_only=True)
    created_by = EmployeeSimpleSerializer(read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = (
            "id",
            "order_number",
            "purchase_request",
            "supplier",
            "status",
            "total_amount",
            "created_by",
        )


class PurchaseOrderDetailSerializer(PurchaseOrderSerializer):
    purchase_request = PurchaseRequestListSerializer(read_only=True)
    supplier = SupplierListSerializer(read_only=True)
    created_by = EmployeeSimpleSerializer(read_only=True)
