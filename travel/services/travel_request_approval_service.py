from django.db import transaction
from rest_framework import serializers

from travel.constants import TravelRequestStatus
from travel.models.travel_request import TravelRequest
from travel.models.travel_request_approval import TravelRequestApproval


class TravelRequestApprovalService:
    @classmethod
    @transaction.atomic
    def approve(cls, *, company, travel_request, employee, remarks=None):
        travel_request = TravelRequest.objects.select_for_update().get(
            company=company,
            pk=travel_request.pk,
        )

        if travel_request.status != TravelRequestStatus.SUBMITTED:
            raise serializers.ValidationError(
                {"status": "Only SUBMITTED requests can be approve."}
            )

        if employee.company_id != company.id:
            raise serializers.ValidationError(
                {"employee": "Employee does not belong to your company."}
            )

        if travel_request.employee_id == employee.id:
            raise serializers.ValidationError(
                {"employee": "You cannot approve your own travel request."}
            )

        approval = TravelRequestApproval.objects.create(
            travel_request=travel_request,
            approved_by=employee,
            remarks=remarks,
            company=company,
        )

        travel_request.status = TravelRequestStatus.APPROVED
        travel_request.save(update_fields=["status"])

        return approval
