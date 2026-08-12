from django.db import transaction
from django.db.models.aggregates import Sum

from django.utils import timezone
from rest_framework import serializers

from inventory.constants import StockReserveStatus
from inventory.models.products import Product
from inventory.models.stock_reservation import StockReservation


class StockReservationService:
    @classmethod
    @transaction.atomic
    def reserve(
        cls,
        *,
        company,
        sales_order,
        product,
        quantity,
        employee,
        expires_at,
    ):
        product = Product.objects.select_for_update().get(
            pk=product.pk, company=company
        )
        stock_reservation = StockReservation.objects.filter(
            company=company, product=product, status=StockReserveStatus.PENDING
        )
        reserved_qty = stock_reservation.aggregate(total=Sum("quantity"))["total"] or 0
        available_stock = product.stock_quantity - reserved_qty

        if available_stock < quantity:
            raise serializers.ValidationError(
                {"quantity": "Insufficient available stock."}
            )

        reservation = StockReservation.objects.create(
            company=company,
            sales_order=sales_order,
            product=product,
            quantity=quantity,
            reserved_by=employee,
            expires_at=expires_at,
        )

        return reservation

    @classmethod
    @transaction.atomic
    def release(cls, *, company, reservation):
        reservation = StockReservation.objects.select_for_update().get(
            pk=reservation.pk, company=company
        )

        if reservation.status != StockReserveStatus.PENDING:
            raise serializers.ValidationError(
                {"status": "Only pending reservations can be released."}
            )

        reservation.status = StockReserveStatus.RELEASED
        reservation.save(update_fields=["status"])

        return reservation

    @classmethod
    @transaction.atomic
    def confirm(cls, *, company, reservation):
        reservation = StockReservation.objects.select_for_update().get(
            pk=reservation.pk, company=company
        )

        if reservation.status != StockReserveStatus.PENDING:
            raise serializers.ValidationError(
                {"status": "Only pending reservations can be confirmed."}
            )

        product = Product.objects.select_for_update().get(
            pk=reservation.product_id, company=company
        )

        product.stock_quantity -= reservation.quantity
        product.save(update_fields=["stock_quantity"])

        reservation.status = StockReserveStatus.CONFIRMED
        reservation.save(update_fields=["status"])

        return reservation

    @classmethod
    @transaction.atomic
    def expire(cls, *, company, reservation):
        reservation = StockReservation.objects.select_for_update().get(
            pk=reservation.pk, company=company
        )

        if reservation.status != StockReserveStatus.PENDING:
            raise serializers.ValidationError(
                {"status": "Only pending should expired."}
            )

        if reservation.expires_at > timezone.now():
            raise serializers.ValidationError(
                {"expires_at": "Reservation has not expired yet."}
            )

        reservation.status = StockReserveStatus.EXPIRED
        reservation.save(update_fields=["status"])

        return reservation
