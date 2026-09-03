from base.views.company_base_view_set import CompanyBaseViewSet
from currency.models.exchange_rate import ExchangeRate
from currency.serializers.exchange_rate_serializer import ExchangeRateDetailSerializer, ExchangeRateListSerializer, ExchangeRateSerializer


class ExchangeRateViewSet(CompanyBaseViewSet):
    model = ExchangeRate
    
    queryset = (
        ExchangeRate.objects
        .select_related("to_currency")
        .prefetch_related(
            "details",
            "details__from_currency",
            "details__rate_category",
        )
    )

    serializer_class = ExchangeRateSerializer
    
    def get_serializer_class(self):
        if self.action == "list":
            return ExchangeRateListSerializer
        
        if self.action == "retrieve":
            return ExchangeRateDetailSerializer
        
        return ExchangeRateSerializer