from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from travel.models.travel_request import TravelRequest
from travel.serializers.travel_request_serializer import TravelRequestDetailSerializer
from travel.services.travel_request_complete_service import TravelRequestCompleteService


class TravelRequestCompleteView(APIView):
    def post(self, request, pk):
        company = request.user.employee.company

        travel_request = get_object_or_404(TravelRequest, pk=pk, company=company)

        travel_request = TravelRequestCompleteService.complete(
            company=company, travel_request=travel_request
        )

        serializer = TravelRequestDetailSerializer(
            travel_request, context={"request": request}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)
