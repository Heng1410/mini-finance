from rest_framework.response import Response
from rest_framework import status

from base.views.company_base_view_set import CompanyBaseViewSet
from transport.models.vehicle_booking import VehicleBooking
from transport.serializers.vehicle_booking_serializer import (
    VehicleBookingDetailSerializer,
    VehicleBookingListSerializer,
    VehicleBookingSerializer,
)
from transport.services.vehicle_booking_service import VehicleBookingService


class VehicleBookingViewSet(CompanyBaseViewSet):
    model = VehicleBooking
    queryset = VehicleBooking.objects.select_related("vehicle", "requester")
    serializer_class = VehicleBookingSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return VehicleBookingListSerializer
        if self.action == "retrieve":
            return VehicleBookingDetailSerializer
        return VehicleBookingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        booking = VehicleBookingService.create_booking(
            company=self.get_company(), **serializer.validated_data
        )

        output_serializer = self.get_serializer(booking)

        return Response(
            output_serializer.data,
            status=status.HTTP_201_CREATED,
        )
