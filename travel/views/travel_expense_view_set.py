from rest_framework.response import Response
from rest_framework import status

from base.views.company_base_view_set import CompanyBaseViewSet
from travel.models.travel_expense import TravelExpense
from travel.serializers.travel_expense_serializer import (
    TravelExpenseDetailSerializer,
    TravelExpenseListSerializer,
    TravelExpenseSerializer,
)


class TravelExpenseViewSet(CompanyBaseViewSet):
    queryset = TravelExpense.objects.select_related(
        "travel_request", "travel_request__destination"
    )
    serializer_class = TravelExpenseSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["company"] = self.get_company()
        return context

    def get_serializer_class(self):
        if self.action == "list":
            return TravelExpenseListSerializer

        if self.action == "retrieve":
            return TravelExpenseDetailSerializer

        return TravelExpenseSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        response_serializer = TravelExpenseDetailSerializer(
            serializer.instance, context=self.get_serializer_context()
        )

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
