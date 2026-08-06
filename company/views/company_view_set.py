from base.views.base_view_set import BaseViewSet
from company.models.company import Company
from company.serializers.company_serializer import (
    CompanyDetailSerializer,
    CompanyListSerializer,
    CompanySerializer,
)


# Create your views here.
class CompanyViewSet(BaseViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def get_serializer_class(self):
        if self.action == "list":
            return CompanyListSerializer
        if self.action == "retrieve":
            return CompanyDetailSerializer

        return CompanySerializer
