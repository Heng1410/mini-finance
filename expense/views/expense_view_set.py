from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response

from base.views.company_base_view_set import CompanyBaseViewSet
from expense.models.expense import Expense
from expense.serializers.expense_serializer import (
    ExpenseDetailSerializer,
    ExpenseListSerializer,
    ExpenseSerializer,
)
from expense.services.expense_service import ExpenseService


class ExpenseViewSet(CompanyBaseViewSet):
    model = Expense

    queryset = Expense.objects.select_related("employee")

    serializer_class = ExpenseSerializer

    filter_backends = CompanyBaseViewSet.filter_backends + (DjangoFilterBackend,)

    filterset_fields = {
        "employee": ["exact"],
        "date": ["exact", "gte", "lte"],
        "category": ["exact"],
        "status": ["exact"],
    }

    search_fields = [
        "employee__first_name",
        "employee__last_name",
        "category",
        "description",
    ]

    def get_serializer_class(self):
        if self.action == "list":
            return ExpenseListSerializer

        if self.action == "retrieve":
            return ExpenseDetailSerializer

        return ExpenseSerializer

    def perform_create(self, serializer):
        employee = self.request.user.employee

        expense = ExpenseService.create_expense(
            employee=employee,
            date=serializer.validated_data["date"],
            category=serializer.validated_data["category"],
            description=serializer.validated_data["description"],
            amount=serializer.validated_data["amount"],
        )

        serializer.instance = expense

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        expense = self.get_object()

        expense = ExpenseService.approve(expense)

        serializer = ExpenseDetailSerializer(expense)

        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        expense = self.get_object()

        expense = ExpenseService.reject(expense)

        serializer = ExpenseDetailSerializer(expense)

        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def reimburse(self, request, pk=None):
        expense = self.get_object()

        expense = ExpenseService.reimburse(expense)

        serializer = ExpenseDetailSerializer(expense)

        return Response(serializer.data)
