from rest_framework import serializers
from django.db import transaction

from travel.constants import TravelRequestStatus
from travel.models.travel_request import TravelRequest


class TravelRequestCompleteService:
    @classmethod
    @transaction.atomic
    def complete(cls, *, company, travel_request):
        travel_request = TravelRequest.objects.select_for_update().get(
            company=company, pk=travel_request.pk
        )

        if travel_request.status != TravelRequestStatus.APPROVED:
            raise serializers.ValidationError(
                {"status": "Only APPROVED requests can be completed."}
            )

        travel_request.status = TravelRequestStatus.COMPLETED
        travel_request.save(update_fields=["status"])

        return travel_request
