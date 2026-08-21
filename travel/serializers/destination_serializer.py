from base.serializers.base_serializer import BaseSerializer
from travel.models.destination import Destination


class DestinationSerializer(BaseSerializer):
    class Meta:
        model = Destination
        fields = ("id", "name", "country", "city", "description", "is_active")


class DestinationListSerializer(BaseSerializer):
    class Meta:
        model = Destination
        fields = ("id", "name", "country", "city", "description", "is_active")
        
class DestinationDetailSerializer(DestinationSerializer):
    pass
