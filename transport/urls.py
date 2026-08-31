from django.urls import include, path
from rest_framework import routers

from transport.views.fuel_transaction_view_set import FuelTransactionViewSet
from transport.views.transport_expense_view_set import TransportExpenseViewSet
from transport.views.transport_passenger_view_set import TransportPassengerViewSet
from transport.views.transport_view_set import TransportViewSet
from transport.views.vehicle_booking_view_set import VehicleBookingViewSet
from transport.views.vehicle_maintenance_view_set import VehicleMaintenanceViewSet
from transport.views.vehicle_view_set import VehicleViewSet

router = routers.DefaultRouter(trailing_slash=False)

router.register(r"transport/vehicle", VehicleViewSet)
router.register(r"transport/vehicle-maintenance", VehicleMaintenanceViewSet)
router.register(r"transport/trips", TransportViewSet)
router.register(r"transport/trips-expense", TransportExpenseViewSet)
router.register(r"transport/passenger", TransportPassengerViewSet)
router.register(r"transport/fuel-transaction",FuelTransactionViewSet)
router.register(r"transport/vehicle-booking", VehicleBookingViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
