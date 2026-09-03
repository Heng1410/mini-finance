from base.views.company_base_view_set import CompanyBaseViewSet
from currency.models.currency import Currency
from currency.serializers.currency_serializer import CurrencyDetailSerializer, CurrencyListSerializer, CurrencySerializer


class CurrencyViewSet(CompanyBaseViewSet):
    model = Currency
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    
    def get_serializer_class(self):
        if self.action == "list":
            return CurrencyListSerializer
        if self.action == "retrieve":
            return CurrencyDetailSerializer
        return CurrencySerializer