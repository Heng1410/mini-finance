from django.db import transaction
from rest_framework import serializers

from employee.models.employee import Employee
from inventory.models.products import Product
from purchase_request.constants import PurchaseRequestStatus
from purchase_request.models.purchase_request import PurchaseRequest
from purchase_request.models.purchase_request_item import PurchaseRequestItem
from sequence.services.sequence_service import SequenceService


class PurchaseRequestService:

    @classmethod
    @transaction.atomic
    def create_request(
        cls,
        *,
        company,
        employee,
        title,
        description,
    ):
        employee = Employee.objects.get(pk=employee.pk, company=company)

        request_number = SequenceService.next(key="PURCHASE_REQUEST", company=company)

        request = PurchaseRequest.objects.create(
            company=company,
            request_number=request_number,
            requested_by=employee,
            title=title,
            description=description,
        )

        return request

    @classmethod
    @transaction.atomic
    def add_item(cls, *, company, request, product, quantity, estimated_unit_price):
        request = PurchaseRequest.objects.select_for_update().get(
            pk=request.pk, company=company, status=PurchaseRequestStatus.DRAFT
        )

        product = Product.objects.get(pk=product.pk, company=company)

        if quantity <= 0:
            raise serializers.ValidationError(
                {"quantity": "Quantity must be greater than zero."}
            )

        if estimated_unit_price < 0:
            raise serializers.ValidationError(
                {"estimated_unit_price": "Estimated unit price cannot be negative."}
            )

        existing_item = PurchaseRequestItem.objects.filter(
            purchase_request=request, product=product
        ).exists()

        if existing_item:
            raise serializers.ValidationError(
                {"product": "Product already exists in this purchase request."}
            )

        estimated_subtotal = quantity * estimated_unit_price

        request_item = PurchaseRequestItem.objects.create(
            company=company,
            purchase_request=request,
            product=product,
            quantity=quantity,
            estimated_unit_price=estimated_unit_price,
            estimated_subtotal=estimated_subtotal,
        )

        return request_item

    @classmethod
    @transaction.atomic
    def submit_request(cls, *, company, request):
        request = PurchaseRequest.objects.select_for_update().get(
            company=company, pk=request.pk
        )

        if request.status != PurchaseRequestStatus.DRAFT:
            raise serializers.ValidationError(
                {"status": "Only DRAFT requests can be submitted."}
            )

        existing_items = PurchaseRequestItem.objects.filter(
            purchase_request=request
        ).exists()

        if not existing_items:
            raise serializers.ValidationError(
                {"items": "At least one item is required."}
            )

        request.status = PurchaseRequestStatus.PENDING
        request.save(update_fields=["status"])

        return request

    @classmethod
    @transaction.atomic
    def approve_request(cls, *, company, request, employee):
        request = PurchaseRequest.objects.select_for_update().get(
            pk=request.pk, company=company
        )

        if request.status != PurchaseRequestStatus.PENDING:
            raise serializers.ValidationError(
                {"status": "Only PENDING requests can be approved."}
            )

        approved_by = Employee.objects.get(pk=employee.pk, company=company)

        request.approved_by = approved_by
        request.status = PurchaseRequestStatus.APPROVED

        request.save(update_fields=["status", "approved_by"])

        return request

    @classmethod
    @transaction.atomic
    def reject_request(cls, *, company, request, employee, rejection_reason):
        request = PurchaseRequest.objects.select_for_update().get(
            pk=request.pk, company=company
        )

        if request.status != PurchaseRequestStatus.PENDING:
            raise serializers.ValidationError(
                {"status": "Only PENDING requests can be rejected."}
            )

        employee = Employee.objects.get(company=company, pk=employee.pk)

        if request.requested_by_id == employee.id:
            raise serializers.ValidationError(
                {"employee": "Employees cannot reject their own purchase requests."}
            )

        if not rejection_reason.strip():
            raise serializers.ValidationError(
                {"rejection_reason": "Rejection can't be empty."}
            )

        request.rejected_by = employee
        request.status = PurchaseRequestStatus.REJECTED
        request.rejected_reason = rejection_reason

        request.save(update_fields=["rejected_by", "status", "rejected_reason"])

        return request
