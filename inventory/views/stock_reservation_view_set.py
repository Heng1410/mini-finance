from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from inventory.services.stock_reservation_service import (
    StockReservationService,
)

from base.views.company_base_view_set import CompanyBaseViewSet
from inventory.models.stock_reservation import StockReservation
from inventory.serializers.stock_reservation_serializer import (
    StockReservationDetailSerializer,
    StockReservationListSerializer,
    StockReservationSerializer,
)


class StockReservationViewSet(CompanyBaseViewSet):
    queryset = StockReservation.objects.all()
    serializer_class = StockReservationSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return StockReservationListSerializer
        if self.action == "retrieve":
            return StockReservationDetailSerializer
        return StockReservationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        reservation = StockReservationService.reserve(
            company=self.get_company(),
            product=serializer.validated_data["product"],
            quantity=serializer.validated_data["quantity"],
            employee=request.user.employee,
            expires_at=serializer.validated_data["expires_at"],
        )

        response_serializer = StockReservationDetailSerializer(reservation)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def release(self, request, pk=None):
        reservation = self.get_object()

        reservation = StockReservationService.release(
            company=self.get_company(),
            reservation=reservation,
        )

        response_serializer = StockReservationDetailSerializer(reservation)

        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def confirm(self, request, pk=None):
        reservation = self.get_object()

        reservation = StockReservationService.confirm(
            company=self.get_company(), reservation=reservation
        )

        response_serializer = StockReservationDetailSerializer(reservation)

        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def expire(self, request, pk=None):
        reservation = self.get_object()

        reservation = StockReservationService.expire(
            company=self.get_company(), reservation=reservation
        )

        response_serializer = StockReservationDetailSerializer(reservation)

        return Response(response_serializer.data, status=status.HTTP_200_OK)
