from django.urls import include, path
from rest_framework import routers

from supplier.views.supplier_view_set import SupplierViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"suppliers", SupplierViewSet)

urlpatterns = [path("", include(router.urls))]
