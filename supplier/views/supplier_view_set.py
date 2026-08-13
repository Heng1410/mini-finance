from base.views.company_base_view_set import CompanyBaseViewSet
from supplier.models.supplier import Supplier
from supplier.serializers.supplier_serializer import (
    SupplierDetailSerializer,
    SupplierListSerializer,
    SupplierSerializer,
)

class SupplierViewSet(CompanyBaseViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return SupplierListSerializer

        if self.action == "retrieve":
            return SupplierDetailSerializer

        return SupplierSerializer
