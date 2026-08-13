from django.urls import include, path
from rest_framework import routers

from purchase_order.views.purchase_order_item_view_set import PurchaseOrderItemViewSet
from purchase_order.views.purchase_order_view_set import PurchaseOrderViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"purchase-orders", PurchaseOrderViewSet)
router.register(r"purchase-order-items", PurchaseOrderItemViewSet)

urlpatterns = [path("", include(router.urls))]
