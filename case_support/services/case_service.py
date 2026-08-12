from django.db import transaction
from rest_framework import serializers

from accounts_receivable.models.customer import Customer
from case_support.constants import CaseStatus
from case_support.models.case import Case
from employee.models.employee import Employee
from sequence.services.sequence_service import SequenceService


class CaseService:
    @classmethod
    @transaction.atomic
    def create_case(cls, *, company, customer, title, description, priority):

        customer = Customer.objects.get(pk=customer.pk, company=company)

        case_number = SequenceService.next(company=company, key="CASE_SUPPORT")

        case = Case.objects.create(
            company=company,
            case_number=case_number,
            title=title,
            description=description,
            priority=priority,
            customer=customer,
        )

        return case

    @classmethod
    @transaction.atomic
    def assign_case(cls, *, company, case, employee):
        case = Case.objects.select_for_update().get(pk=case.id, company=company)

        if case.status != CaseStatus.OPEN:
            raise serializers.ValidationError(
                {"status": "Only OPEN cases can be assigned."}
            )

        employee = Employee.objects.get(pk=employee.pk, company=company)

        case.status = CaseStatus.ASSIGNED
        case.assigned_to = employee
        case.save(update_fields=["assigned_to", "status"])

        return case

    @classmethod
    @transaction.atomic
    def start_case(cls, *, company, case):
        case = Case.objects.select_for_update().get(pk=case.id, company=company)

        if case.status != CaseStatus.ASSIGNED:
            raise serializers.ValidationError(
                {"status": "Only ASSIGNED cases can be start."}
            )

        case.status = CaseStatus.IN_PROGRESS
        case.save(update_fields=["status"])

        return case

    @classmethod
    @transaction.atomic
    def resolve_case(cls, *, company, case, resolution_note):
        case = Case.objects.select_for_update().get(pk=case.pk, company=company)

        if case.status != CaseStatus.IN_PROGRESS:
            raise serializers.ValidationError(
                {"status": "Only IN_PROGRESS cases can be resolve."}
            )

        if not resolution_note.strip():
            raise serializers.ValidationError(
                {"resolution_note": "Resolution note is required."}
            )

        case.resolution_note = resolution_note
        case.status = CaseStatus.RESOLVED
        case.save(update_fields=["status", "resolution_note"])

        return case

    @classmethod
    @transaction.atomic
    def close_case(cls, *, company, case):
        case = Case.objects.select_for_update().get(pk=case.pk, company=company)

        if case.status != CaseStatus.RESOLVED:
            raise serializers.ValidationError(
                {"status": "Only RESOLVED cases can be closed."}
            )

        case.status = CaseStatus.CLOSED
        case.save(update_fields=["status"])

        return case
