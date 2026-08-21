from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from travel.models.travel_request import TravelRequest
from travel.serializers.travel_request_rejection_serializer import (
    TravelRequestRejectionDetailSerializer,
    TravelRequestRejectionSerializer,
)
from travel.services.travel_request_rejection_service import (
    TravelRequestRejectionService,
)


class TravelRequestRejectView(APIView):
    def post(self, request, pk):
        company = request.user.employee.company

        serializer = TravelRequestRejectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        travel_request = get_object_or_404(TravelRequest, pk=pk, company=company)

        travel_request_rejection = TravelRequestRejectionService.reject(
            travel_request=travel_request,
            company=company,
            employee=request.user.employee,
            remarks=serializer.validated_data.get("remarks"),
        )

        serializer = TravelRequestRejectionDetailSerializer(
            travel_request_rejection, context={"request": request}
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
