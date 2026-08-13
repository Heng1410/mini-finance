from django.db import transaction
from rest_framework import serializers

from employee.models.employee import Employee
from inventory.models.products import Product
from purchase_order.constants import PurchaseOrderStatus
from purchase_order.models.purchase_order import PurchaseOrder
from purchase_order.models.purchase_order_item import PurchaseOrderItem
from purchase_request.constants import PurchaseRequestStatus
from purchase_request.models.purchase_request import PurchaseRequest
from sequence.services.sequence_service import SequenceService
from supplier.models.supplier import Supplier


class PurchaseOrderService:

    @classmethod
    @transaction.atomic
    def create_order(cls, *, company, purchase_request, supplier, employee):

        purchase_request = PurchaseRequest.objects.select_for_update().get(
            pk=purchase_request.pk,
            company=company,
        )

        if purchase_request.status != PurchaseRequestStatus.APPROVED:
            raise serializers.ValidationError(
                {"status": "Only APPROVED requests can create a purchase order."}
            )

        supplier = Supplier.objects.get(pk=supplier.pk, company=company)

        created_by = Employee.objects.get(pk=employee.pk, company=company)

        existing_order = PurchaseOrder.objects.filter(
            purchase_request=purchase_request,
            company=company,
        ).exists()

        if existing_order:
            raise serializers.ValidationError(
                {
                    "purchase_request": "A purchase order already exists for this request."
                }
            )

        order_number = SequenceService.next(key="PURCHASE_ORDERSS", company=company)

        order = PurchaseOrder.objects.create(
            company=company,
            order_number=order_number,
            purchase_request=purchase_request,
            supplier=supplier,
            total_amount=0,
            created_by=created_by,
        )

        return order

    @classmethod
    @transaction.atomic
    def add_item(cls, *, company, purchase_order, product, quantity, unit_price):
        purchase_order = PurchaseOrder.objects.select_for_update().get(
            pk=purchase_order.pk, company=company
        )

        if purchase_order.status != PurchaseOrderStatus.DRAFT:
            raise serializers.ValidationError(
                {"status": "Only DRAFT requests can add a purchase items."}
            )

        product = Product.objects.get(pk=product.pk, company=company)

        if quantity <= 0:
            raise serializers.ValidationError(
                {"quantity": "Quantity must be greater than 0."}
            )

        if unit_price <= 0:
            raise serializers.ValidationError(
                {"unit_price": "Unit price must be greater than 0."}
            )

        existing_product = PurchaseOrderItem.objects.filter(
            purchase_order=purchase_order, product=product
        ).exists()

        if existing_product:
            raise serializers.ValidationError(
                {"product": "Product already exists in this purchase order."}
            )

        sub_total = quantity * unit_price

        purchase_order_item = PurchaseOrderItem.objects.create(
            company=company,
            purchase_order=purchase_order,
            product=product,
            quantity=quantity,
            unit_price=unit_price,
            sub_total=sub_total,
        )

        purchase_order.total_amount += sub_total
        purchase_order.save(update_fields=["total_amount"])

        return purchase_order_item
