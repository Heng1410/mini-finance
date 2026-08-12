from django.shortcuts import render

from base.views.company_base_view_set import CompanyBaseViewSet
from inventory.models.products import Product
from inventory.serializers.product_serializer import (
    ProductDetailSerializer,
    ProductListSerializer,
    ProductSerializer,
)


# Create your views here.
class ProductViewSet(CompanyBaseViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer

        if self.action == "retrieve":
            return ProductDetailSerializer

        return ProductSerializer
