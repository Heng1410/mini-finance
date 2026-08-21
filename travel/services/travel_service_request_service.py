from rest_framework import serializers
from django.db import transaction

from travel.constants import TravelRequestStatus
from travel.models.travel_request import TravelRequest


class TravelRequestService:
    @classmethod
    @transaction.atomic
    def submit(cls, *, company, travel_request):
        travel_request = TravelRequest.objects.select_for_update().get(
            pk=travel_request.pk, company=company
        )

        if travel_request.status != TravelRequestStatus.DRAFT:
            raise serializers.ValidationError(
                {"status": "Only DRAFT requests can be submitted."}
            )

        travel_request.status = TravelRequestStatus.SUBMITTED
        travel_request.save(update_fields=["status"])

        return travel_request
