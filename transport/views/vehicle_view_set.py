from django.shortcuts import render

from base.views.company_base_view_set import CompanyBaseViewSet
from transport.models.vehicle import Vehicle
from transport.serializers.vehicle_serializer import (
    VehicleDetailSerializer,
    VehicleListSerializer,
    VehicleSerializer,
)


# Create your views here.
class VehicleViewSet(CompanyBaseViewSet):
    model = Vehicle
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    def get_queryset(self):
        queryset = Vehicle.objects.select_related("driver").all()

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return VehicleListSerializer
        if self.action == "retrieve":
            return VehicleDetailSerializer
        return VehicleSerializer
