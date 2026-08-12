from rest_framework import serializers
from django.db import transaction

from inventory.constants import StockMovementType
from inventory.models.products import Product
from inventory.models.stock_movement import StockMovement


class StockMovementService:
    @classmethod
    @transaction.atomic
    def create_movement(
        cls,
        *,
        company,
        product,
        movement_type,
        quantity,
        employee,
        reference="",
        note="",
    ):
        if quantity <= 0:
            raise serializers.ValidationError(
                {"quantity": "Quantity must be greater than zero."}
            )

        product = Product.objects.select_for_update().get(
            pk=product.pk, company=company
        )
        stock_in_types = {
            StockMovementType.PURCHASE,
            StockMovementType.INITIAL,
            StockMovementType.ADJUSTMENT_IN,
        }

        stock_out_types = {
            StockMovementType.SALE,
            StockMovementType.DAMAGE,
            StockMovementType.ADJUSTMENT_OUT,
        }

        if movement_type in stock_in_types:
            new_stock = product.stock_quantity + quantity
        elif movement_type in stock_out_types:
            new_stock = product.stock_quantity - quantity

            if new_stock < 0:
                raise serializers.ValidationError({"quantity": "Insufficient stock."})

        else:
            raise serializers.ValidationError(
                {"movement_type": "Invalid stock movement type."}
            )

        product.stock_quantity = new_stock
        product.save(update_fields=["stock_quantity"])

        movement = StockMovement.objects.create(
            company=company,
            product=product,
            movement_type=movement_type,
            quantity=quantity,
            performed_by=employee,
            reference=reference,
            note=note,
        )

        return movement

    @classmethod
    @transaction.atomic
    def adjust_stock(
        cls,
        *,
        company,
        product,
        actual_quantity,
        employee,
        reference="",
        note="",
    ):
        if actual_quantity < 0:
            raise serializers.ValidationError(
                {"actual_quantity": "Actual quantity cannot be negative."}
            )
        product = Product.objects.select_for_update().get(
            pk=product.pk, company=company
        )

        current_stock = product.stock_quantity
        difference = actual_quantity - current_stock

        if difference > 0:
            movement_type = StockMovementType.ADJUSTMENT_IN
            quantity = difference

        elif difference < 0:
            movement_type = StockMovementType.ADJUSTMENT_OUT
            quantity = abs(difference)

        else:
            return None

        return cls.create_movement(
            company=company,
            product=product,
            movement_type=movement_type,
            quantity=quantity,
            employee=employee,
            reference=reference,
            note=note,
        )
