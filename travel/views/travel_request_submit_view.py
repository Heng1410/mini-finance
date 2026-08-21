from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from travel.models.travel_request import TravelRequest
from travel.serializers.travel_request_serializer import TravelRequestDetailSerializer
from travel.services.travel_service_request_service import TravelRequestService


class TravelRequestSubmitView(APIView):
    def post(self, request, pk):
        company = request.user.employee.company

        travel_request = get_object_or_404(TravelRequest, pk=pk, company=company)

        travel_request = TravelRequestService.submit(
            company=company, travel_request=travel_request
        )

        serializer = TravelRequestDetailSerializer(
            travel_request,
            context={"request": request},
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
