from base.views.company_base_view_set import CompanyBaseViewSet
from transport.models.transport_passenger import TransportPassenger
from transport.serializers.transport_passenger_serializer import (
    TransportPassengerDetailSerializer,
    TransportPassengerListSerializer,
    TransportPassengerSerializer,
)


class TransportPassengerViewSet(CompanyBaseViewSet):
    model = TransportPassenger
    queryset = TransportPassenger.objects.select_related("transport", "employee")
    serializer_class = TransportPassengerSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return TransportPassengerListSerializer
        if self.action == "retrieve":
            return TransportPassengerDetailSerializer
        return TransportPassengerSerializer
