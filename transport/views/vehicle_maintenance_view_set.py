from base.views.company_base_view_set import CompanyBaseViewSet
from transport.models.vehicle_maintenance import VehicleMaintenance
from transport.serializers.vehicle_maintenance_serializer import (
    VehicleDetailMaintenanceSerializer,
    VehicleListMaintenanceSerializer,
    VehicleMaintenanceSerializer,
)
from transport.services.vehicle_booking_service import VehicleBookingService


class VehicleMaintenanceViewSet(CompanyBaseViewSet):
    model = VehicleMaintenance
    queryset = VehicleMaintenance.objects.select_related("vehicle")
    serializer_class = VehicleMaintenanceSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return VehicleListMaintenanceSerializer
        if self.action == "retrieve":
            return VehicleDetailMaintenanceSerializer
        return VehicleMaintenanceSerializer
