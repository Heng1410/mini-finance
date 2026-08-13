from rest_framework.response import Response
from rest_framework import status

from base.views.company_base_view_set import CompanyBaseViewSet
from purchase_order.models.purchase_order import PurchaseOrder
from purchase_order.serializers.purchase_order_serializer import (
    PurchaseOrderDetailSerializer,
    PurchaseOrderListSerializer,
    PurchaseOrderSerializer,
)
from purchase_order.services.purchase_order_service import PurchaseOrderService


# Create your views here.
class PurchaseOrderViewSet(CompanyBaseViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return PurchaseOrderListSerializer

        if self.action == "retrieve":
            return PurchaseOrderDetailSerializer

        return PurchaseOrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        purchase_order = PurchaseOrderService.create_order(
            company=self.get_company(),
            purchase_request=serializer.validated_data["purchase_request"],
            supplier=serializer.validated_data["supplier"],
            employee=request.user.employee,
        )

        response_serializer = PurchaseOrderDetailSerializer(purchase_order)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )
