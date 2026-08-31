from base.views.company_base_view_set import CompanyBaseViewSet
from transport.models.fuel_transaction import FuelTransaction
from transport.serializers.fuel_transaction_serializer import FuelTransactionDetailSerializer, FuelTransactionListSerializer, FuelTransactionSerializer


class FuelTransactionViewSet(CompanyBaseViewSet):
    model = FuelTransaction
    queryset = FuelTransaction.objects.select_related("vehicle")
    serializer_class = FuelTransactionSerializer
    
    def get_serializer_class(self):
        if self.action == "list":
            return FuelTransactionListSerializer
        if self.action == "retrieve":
            return FuelTransactionDetailSerializer
        return FuelTransactionSerializer