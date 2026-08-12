from django.utils import timezone
from celery import shared_task

from inventory.constants import StockReserveStatus
from inventory.models.stock_reservation import StockReservation
from inventory.services.stock_reservation_service import StockReservationService


@shared_task
def expire_stock_reservations():
    reservations = StockReservation.objects.filter(
        status=StockReserveStatus.PENDING,
        expires_at__lte=timezone.now(),
    )
    for reservation in reservations:
        StockReservationService.expire(
            company=reservation.company,
            reservation=reservation,
        )
