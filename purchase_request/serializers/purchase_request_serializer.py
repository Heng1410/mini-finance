from base.serializers.base_serializer import BaseSerializer
from employee.serializers.employee_serializer import EmployeeSimpleSerializer
from purchase_request.models.purchase_request import PurchaseRequest


class PurchaseRequestSerializer(BaseSerializer):
    class Meta:
        model = PurchaseRequest
        fields = (
            "id",
            "request_number",
            "requested_by",
            "title",
            "description",
            "status",
            "approved_by",
            "rejected_by",
            "rejected_reason",
        )
        read_only_fields = ("id", "request_number", "requested_by", "status")


class PurchaseRequestListSerializer(BaseSerializer):
    requested_by = EmployeeSimpleSerializer(read_only=True)
    approved_by = EmployeeSimpleSerializer(read_only=True)
    rejected_by = EmployeeSimpleSerializer(read_only=True)

    class Meta:
        model = PurchaseRequest
        fields = (
            "id",
            "request_number",
            "requested_by",
            "title",
            "status",
            "approved_by",
            "rejected_by",
            "rejected_reason",
        )


class PurchaseRequestDetailSerializer(PurchaseRequestSerializer):
    requested_by = EmployeeSimpleSerializer(read_only=True)
    approved_by = EmployeeSimpleSerializer(read_only=True)
    rejected_by = EmployeeSimpleSerializer(read_only=True)
