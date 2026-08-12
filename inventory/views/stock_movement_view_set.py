from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from rest_framework.response import Response
from rest_framework import status

from base.views.company_base_view_set import CompanyBaseViewSet
from inventory.models.stock_movement import StockMovement
from inventory.serializers.stock_adjustment_serializer import StockAdjustmentSerializer
from inventory.serializers.stock_movement_serializer import (
    StockMovementDetailSerializer,
    StockMovementListSerializer,
    StockMovementSerializer,
)
from inventory.services.stock_movement_service import StockMovementService


class StockMovementViewSet(CompanyBaseViewSet):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return StockMovementListSerializer
        if self.action == "retrieve":
            return StockMovementDetailSerializer
        return StockMovementSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        stock_movement = StockMovementService.create_movement(
            company=self.get_company(),
            product=serializer.validated_data["product"],
            movement_type=serializer.validated_data["movement_type"],
            quantity=serializer.validated_data["quantity"],
            employee=request.user.employee,
            reference=serializer.validated_data.get("reference", ""),
            note=serializer.validated_data.get("note", ""),
        )

        response_serializer = StockMovementDetailSerializer(stock_movement)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"])
    def adjust(self, request, pk=None):
        serializer = StockAdjustmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        stock_movement = StockMovementService.adjust_stock(
            company=self.get_company(),
            product=serializer.validated_data["product"],
            actual_quantity=serializer.validated_data["actual_quantity"],
            employee=request.user.employee,
            reference=serializer.validated_data.get("reference", ""),
            note=serializer.validated_data.get("note", ""),
        )

        if stock_movement is None:
            return Response(
                {"message": "Stock is already accurate. No adjustment needed."},
                status=status.HTTP_200_OK,
            )

        response_serializer = StockMovementDetailSerializer(stock_movement)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
