from base.views.company_base_view_set import CompanyBaseViewSet
from transport.models.transport_expense import TransportExpense
from transport.serializers.transport_expense_serializer import (
    TransportExpenseDetailSerializer,
    TransportExpenseListSerializer,
    TransportExpenseSerializer,
)


class TransportExpenseViewSet(CompanyBaseViewSet):
    queryset = TransportExpense.objects.select_related("transport")
    serializer_class = TransportExpenseSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return TransportExpenseListSerializer
        if self.action == "retrieve":
            return TransportExpenseDetailSerializer
        return TransportExpenseSerializer
