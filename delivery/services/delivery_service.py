from decimal import Decimal
from django.utils import timezone

from django.db import models, transaction
from rest_framework import serializers

from delivery.constants import DeliveryStatus
from delivery.models.delivery import Delivery
from delivery.models.delivery_item import DeliveryItem
from inventory.constants import StockMovementType
from inventory.services.stock_movement_service import StockMovementService
from sales_order.constants import SalesOrderStatus
from sales_order.models.sales_order import SalesOrder
from sales_order.models.sales_order_item import SalesOrderItem
from sequence.services.sequence_service import SequenceService


class DeliveryService:
    @classmethod
    @transaction.atomic
    def create_delivery(
        cls, *, company, sales_order, delivery_date, employee, notes=""
    ):
        sales_order = SalesOrder.objects.get(pk=sales_order.pk, company=company)

        if sales_order.status != SalesOrderStatus.CONFIRMED:
            raise serializers.ValidationError(
                {"sales_order": ("Only confirmed sales orders can create a delivery.")}
            )

        delivery_number = SequenceService.next(company=company, key="DELIVERY")

        delivery = Delivery.objects.create(
            company=company,
            delivery_number=delivery_number,
            sales_order=sales_order,
            status=DeliveryStatus.DRAFT,
            delivery_date=delivery_date,
            created_by=employee,
            notes=notes,
        )

        return delivery

    @classmethod
    @transaction.atomic
    def add_item(cls, *, company, delivery, sales_order_item, quantity):
        delivery = Delivery.objects.select_for_update().get(
            pk=delivery.pk, company=company
        )

        if delivery.status != DeliveryStatus.DRAFT:
            raise serializers.ValidationError(
                {"delivery": "Only draft deliveries can have items added."}
            )

        sales_order_item = SalesOrderItem.objects.get(
            pk=sales_order_item.pk, company=company, sales_order=delivery.sales_order
        )

        if quantity <= 0:
            raise serializers.ValidationError(
                {"quantity": "Quantity must be greater than zero."}
            )

        existing_item = DeliveryItem.objects.filter(
            delivery=delivery,
            sales_order_item=sales_order_item,
        ).exists()

        if existing_item:
            raise serializers.ValidationError(
                {
                    "sales_order_item": (
                        "Sales order item already exists in this delivery."
                    )
                }
            )

        delivered_quantity = DeliveryItem.objects.filter(
            sales_order_item=sales_order_item,
            company=company,
        ).aggregate(total=models.Sum("quantity"))["total"] or Decimal("0")

        remaining_quantity = sales_order_item.quantity - delivered_quantity

        if quantity > remaining_quantity:
            raise serializers.ValidationError(
                {
                    "quantity": (
                        f"Cannot deliver more than the remaining quantity. "
                        f"Remaining quantity: {remaining_quantity}."
                    )
                }
            )

        unit_price = sales_order_item.unit_price
        amount = quantity * unit_price

        return DeliveryItem.objects.create(
            company=company,
            delivery=delivery,
            sales_order_item=sales_order_item,
            product=sales_order_item.product,
            quantity=quantity,
            unit_price=unit_price,
            amount=amount,
        )

    @classmethod
    @transaction.atomic
    def confirm_delivery(cls, *, company, delivery, employee):
        delivery = Delivery.objects.select_for_update().get(
            pk=delivery.pk, company=company
        )

        if delivery.status != DeliveryStatus.DRAFT:
            raise serializers.ValidationError(
                {"delivery": "Only draft deliveries can be confirmed."}
            )

        if not delivery.items.exists():
            raise serializers.ValidationError(
                {"items": "Delivery must have at least one item."}
            )

        sales_order = SalesOrder.objects.select_for_update().get(
            pk=delivery.sales_order_id,
            company=company,
        )

        if sales_order.status != SalesOrderStatus.CONFIRMED:
            raise serializers.ValidationError(
                {"sales_order": ("Only confirmed sales orders can be delivered.")}
            )

        delivery_items = DeliveryItem.objects.select_for_update().filter(
            delivery=delivery, company=company
        )

        for delivery_item in delivery_items:
            sales_order_item = SalesOrderItem.objects.select_for_update().get(
                pk=delivery_item.sales_order_item_id,
                company=company,
                sales_order=sales_order,
            )

            delivered_quantity = DeliveryItem.objects.filter(
                sales_order_item=sales_order_item, company=company
            ).exclude(delivery=delivery).aggregate(total=models.Sum("quantity"))[
                "total"
            ] or Decimal(
                "0"
            )

            remaining_quantity = sales_order_item.quantity - delivered_quantity

            if delivery_item.quantity > remaining_quantity:
                raise serializers.ValidationError(
                    {
                        "quantity": (
                            f"Cannot deliver more than the remaining quantity "
                            f"for product {delivery_item.product_id}. "
                            f"Remaining quantity: {remaining_quantity}."
                        )
                    }
                )

            StockMovementService.create_movement(
                company=company,
                product=delivery_item.product,
                movement_type=StockMovementType.SALE,
                quantity=delivery_item.quantity,
                employee=employee,
                reference=delivery.delivery_number,
                note=f"delivery {delivery.delivery_number}",
            )

        delivery.status = DeliveryStatus.CONFIRMED
        delivery.confirmed_by = employee
        delivery.confirmed_at = timezone.now()

        delivery.save(update_fields=["status", "confirmed_by", "confirmed_at"])

        cls.update_sales_order_status(sales_order=sales_order)

        return delivery

    @classmethod
    def update_sales_order_status(cls, *, sales_order):
        sales_order_items = SalesOrderItem.objects.filter(
            sales_order=sales_order,
            company=sales_order.company,
        )

        for sales_order_item in sales_order_items:
            delivered_quantity = DeliveryItem.objects.filter(
                sales_order_item=sales_order_item, company=sales_order.company
            ).aggregate(total=models.Sum("quantity"))["total"] or Decimal("0")

            if delivered_quantity < sales_order_item.quantity:
                return

        sales_order.status = SalesOrderStatus.COMPLETED
        sales_order.save(update_fields=["status"])
