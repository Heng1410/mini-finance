from base.views.company_base_view_set import CompanyBaseViewSet
from transport.models.transport import Transport
from transport.serializers.transport_serializer import (
    TransportDetailSerializer,
    TransportListSerializer,
    TransportSerializer,
)


class TransportViewSet(CompanyBaseViewSet):
    queryset = Transport.objects.select_related("vehicle", "driver")
    serializer_class = TransportSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return TransportListSerializer
        if self.action == "retrieve":
            return TransportDetailSerializer
        return TransportSerializer
