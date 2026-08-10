from base.views.company_base_view_set import CompanyBaseViewSet
from sequence.models.sequence import Sequence
from sequence.serializers.sequence_serializer import SequenceSerializer


class SequenceViewSet(CompanyBaseViewSet):
    queryset = Sequence.objects.all()
    serializer_class = SequenceSerializer
