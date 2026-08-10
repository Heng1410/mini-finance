from base.views.company_base_view_set import CompanyBaseViewSet
from accounts_receivable.models.customer import Customer
from accounts_receivable.serializers.customer_serializer import (
    CustomerDetailSerializer,
    CustomerListSerializer,
    CustomerSerializer,
)


class CustomerViewSet(CompanyBaseViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return CustomerListSerializer
        if self.action == "retrieve":
            return CustomerDetailSerializer
        return CustomerSerializer
