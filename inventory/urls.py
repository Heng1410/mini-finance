from django.urls import include, path
from rest_framework import routers

from inventory.views.product_view_set import ProductViewSet
from inventory.views.stock_movement_view_set import StockMovementViewSet
from inventory.views.stock_reservation_view_set import StockReservationViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"products", ProductViewSet)
router.register(r"stock-reservations", StockReservationViewSet)
router.register(r"stock-movements", StockMovementViewSet)

urlpatterns = [path("", include(router.urls))]
