from django.urls import include, path
from rest_framework import routers

from purchase_request.views.purchase_request_item_view_set import (
    PurchaseRequestItemViewSet,
)
from purchase_request.views.purchase_request_view_set import PurchaseRequestViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"purchase-requests", PurchaseRequestViewSet)
router.register(r"purchase-request-items", PurchaseRequestItemViewSet)

urlpatterns = [path("", include(router.urls))]
