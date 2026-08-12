from django.db import transaction
from rest_framework import serializers

from datetime import timedelta
from django.utils import timezone

from accounts_receivable.models.customer import Customer
from inventory.constants import StockReserveStatus
from inventory.models.products import Product
from inventory.models.stock_reservation import StockReservation
from inventory.services.stock_reservation_service import StockReservationService
from sales_order.constants import SalesOrderStatus
from sales_order.models.sales_order import SalesOrder
from sales_order.models.sales_order_item import SalesOrderItem
from sequence.services.sequence_service import SequenceService


class SalesOrderService:
    @classmethod
    @transaction.atomic
    def create_order(cls, *, company, customer, employee):
        customer = Customer.objects.get(pk=customer.pk, company=company)
        order_number = SequenceService.next(company=company, key="SALES_ORDER")

        order = SalesOrder.objects.create(
            company=company,
            customer=customer,
            order_number=order_number,
            created_by=employee,
        )

        return order

    @classmethod
    @transaction.atomic
    def add_item(cls, *, company, order, product, quantity, unit_price):
        order = SalesOrder.objects.get(pk=order.id, company=company)
        if order.status != SalesOrderStatus.DRAFT:
            raise serializers.ValidationError("Only draft orders can have items added.")

        product = Product.objects.get(pk=product.id, company=company)

        if quantity <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")

        existing_item = SalesOrderItem.objects.filter(
            sales_order=order,
            product=product,
        ).exists()

        if existing_item:
            raise serializers.ValidationError(
                {"product": "Product already exists in this order."}
            )

        if unit_price < 0:
            raise serializers.ValidationError(
                {"unit_price": "Unit price cannot be negative."}
            )

        sub_total = quantity * unit_price

        sales_order_item = SalesOrderItem.objects.create(
            company=company,
            sales_order=order,
            product=product,
            quantity=quantity,
            unit_price=unit_price,
            sub_total=sub_total,
        )

        order.total_amount += sub_total
        order.save(update_fields=["total_amount"])

        return sales_order_item

    @classmethod
    @transaction.atomic
    def submit_order(cls, *, company, order, employee):
        order = SalesOrder.objects.select_for_update().get(pk=order.pk, company=company)
        if order.status != SalesOrderStatus.DRAFT:
            raise serializers.ValidationError(
                {"status": "Only draft orders can be submitted."}
            )

        items = SalesOrderItem.objects.select_for_update().filter(
            sales_order=order,
            company=company,
        )

        if not items.exists():
            raise serializers.ValidationError(
                {"items": "Order must have at least one item."}
            )

        expires_at = timezone.now() + timedelta(minutes=30)

        for item in items:
            StockReservationService.reserve(
                company=company,
                employee=employee,
                expires_at=expires_at,
                product=item.product,
                quantity=item.quantity,
                sales_order=order,
            )

        order.status = SalesOrderStatus.PENDING
        order.save(update_fields=["status"])

        return order

    @classmethod
    @transaction.atomic
    def confirm_order(cls, *, company, order):
        sales_order = SalesOrder.objects.select_for_update().get(
            pk=order.pk, company=company
        )

        if sales_order.status != SalesOrderStatus.PENDING:
            raise serializers.ValidationError(
                {"status": "Only pending orders can be confirmed."}
            )

        stock_reservations = StockReservation.objects.select_for_update().filter(
            sales_order=sales_order,
            company=company,
            status=StockReserveStatus.PENDING,
        )

        if not stock_reservations.exists():
            raise serializers.ValidationError(
                {
                    "stock_reservations": "Order must have at least one stock reservation."
                }
            )

        for reservation in stock_reservations:
            StockReservationService.confirm(company=company, reservation=reservation)

        sales_order.status = SalesOrderStatus.CONFIRMED
        sales_order.save(update_fields=["status"])

        return sales_order

    @classmethod
    @transaction.atomic
    def cancel_order(cls, *, company, order):
        order = SalesOrder.objects.select_for_update().get(pk=order.pk, company=company)

        if order.status != SalesOrderStatus.PENDING:
            raise serializers.ValidationError(
                {"status": "Only pending orders can be cancelled."}
            )

        stock_reservations = StockReservation.objects.select_for_update().filter(
            sales_order=order,
            company=company,
            status=StockReserveStatus.PENDING,
        )

        if not stock_reservations.exists():
            raise serializers.ValidationError(
                {
                    "stock_reservations": "Order must have at least one stock reservation."
                }
            )

        for reservation in stock_reservations:
            StockReservationService.release(
                company=company,
                reservation=reservation,
            )

        order.status = SalesOrderStatus.CANCELLED
        order.save(update_fields=["status"])

        return order
