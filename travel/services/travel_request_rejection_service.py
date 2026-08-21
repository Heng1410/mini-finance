from django.db import transaction
from rest_framework import serializers

from travel.constants import TravelRequestStatus
from travel.models.travel_request import TravelRequest
from travel.models.travel_request_rejection import TravelRequestRejection


class TravelRequestRejectionService:
    @classmethod
    @transaction.atomic
    def reject(cls, *, company, travel_request, employee, remarks=None):
        travel_request = TravelRequest.objects.select_for_update().get(
            pk=travel_request.pk, company=company
        )

        if travel_request.status != TravelRequestStatus.SUBMITTED:
            raise serializers.ValidationError(
                {"status": "Only SUBMITTED requests can be rejected."}
            )

        if employee.company_id != company.id:
            raise serializers.ValidationError(
                {"employee": "Employee does not belong to your company."}
            )

        if travel_request.employee_id == employee.id:
            raise serializers.ValidationError(
                {"employee": "You cannot reject your own travel request."}
            )

        rejection = TravelRequestRejection.objects.create(
            travel_request=travel_request,
            rejected_by=employee,
            company=company,
            remarks=remarks,
        )

        travel_request.status = TravelRequestStatus.REJECTED
        travel_request.save(update_fields=["status"])

        return rejection
