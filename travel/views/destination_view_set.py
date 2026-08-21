from base.views.company_base_view_set import CompanyBaseViewSet
from travel.models.destination import Destination
from travel.serializers.destination_serializer import (
    DestinationDetailSerializer,
    DestinationListSerializer,
    DestinationSerializer,
)


class DestinationViewSet(CompanyBaseViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return DestinationListSerializer

        if self.action == "retrieve":
            return DestinationDetailSerializer

        return DestinationSerializer
