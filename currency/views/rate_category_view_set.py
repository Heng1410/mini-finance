from base.views.company_base_view_set import CompanyBaseViewSet
from currency.models.rate_category import RateCategory
from currency.serializers.rate_category_serializer import (
    RateCategoryDetailSerializer,
    RateCategoryListSerializer,
    RateCategorySerializer,
)


class RateCategoryViewSet(CompanyBaseViewSet):
    model = RateCategory
    queryset = RateCategory.objects.all()
    serializer_class = RateCategorySerializer

    def get_serializer_class(self):
        if self.action == "list":
            return RateCategoryListSerializer
        if self.action == "retrieve":
            return RateCategoryDetailSerializer
        return RateCategorySerializer
