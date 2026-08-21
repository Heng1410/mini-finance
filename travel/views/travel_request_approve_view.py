from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from travel.models.travel_request import TravelRequest
from travel.serializers.travel_request_approval_serializer import (
    TravelRequestApprovalDetailSerializer,
    TravelRequestApprovalSerializer,
)
from travel.services.travel_request_approval_service import TravelRequestApprovalService


class TravelRequestApproveView(APIView):
    def post(self, request, pk):
        company = request.user.employee.company

        serializer = TravelRequestApprovalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        travel_request = get_object_or_404(TravelRequest, pk=pk, company=company)

        travel_request_approval = TravelRequestApprovalService.approve(
            travel_request=travel_request,
            company=company,
            employee=request.user.employee,
            remarks=serializer.validated_data.get("remarks"),
        )

        serializer = TravelRequestApprovalDetailSerializer(
            travel_request_approval,
            context={"request": request},
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
