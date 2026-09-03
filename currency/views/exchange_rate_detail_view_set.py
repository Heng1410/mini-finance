from base.views.company_base_view_set import CompanyBaseViewSet
from currency.models.exchange_rate_detail import ExchangeRateDetail
from currency.serializers.exchange_rate_detail_serializer import (
    ExchangeRateDetailDetailSerializer,
    ExchangeRateDetailListSerializer,
    ExchangeRateDetailSerializer,
)


class ExchangeRateDetailViewSet(CompanyBaseViewSet):
    model = ExchangeRateDetail
    queryset = ExchangeRateDetail.objects.select_related(
        "exchange_rate",
        "from_currency",
        "rate_category",
    )
    serializer_class = ExchangeRateDetailSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return ExchangeRateDetailListSerializer

        if self.action == "retrieve":
            return ExchangeRateDetailDetailSerializer

        return ExchangeRateDetailSerializer
