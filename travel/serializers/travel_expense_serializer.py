from rest_framework import serializers

from base.serializers.base_serializer import BaseSerializer
from travel.constants import TravelRequestStatus
from travel.models.travel_expense import TravelExpense
from travel.models.travel_request import TravelRequest
from travel.serializers.travel_request_serializer import TravelRequestSimpleSerializer


class TravelExpenseSerializer(BaseSerializer):
    travel_request = serializers.PrimaryKeyRelatedField(
        queryset=TravelRequest.objects.all()
    )

    class Meta:
        model = TravelExpense
        fields = (
            "id",
            "travel_request",
            "expense_date",
            "category",
            "amount",
            "description",
        )
        read_only_fields = ("id",)

    def validate(self, attrs):
        travel_request = attrs.get("travel_request")

        if self.instance and travel_request is None:
            travel_request = self.instance.travel_request

        if self.instance and "travel_request" in attrs:
            if attrs["travel_request"].id != self.instance.travel_request.id:
                raise serializers.ValidationError(
                    {"travel_request": "Travel request cannot be changed."}
                )

        expense_date = attrs.get(
            "expense_date", self.instance.expense_date if self.instance else None
        )

        amount = attrs.get(
            "amount",
            self.instance.amount if self.instance else None,
        )

        company = self.context["company"]

        start_date = travel_request.start_date.date()
        end_date = travel_request.end_date.date()

        if travel_request.company_id != company.id:
            raise serializers.ValidationError(
                {"travel_request": "Travel request does not belong to your company."}
            )

        if travel_request.status != TravelRequestStatus.APPROVED:
            raise serializers.ValidationError(
                {"travel_request": "Only approved travel requests can have expenses."}
            )

        if expense_date and expense_date < start_date:
            raise serializers.ValidationError(
                {"expense_date": "Expense date cannot be before travel start date."}
            )

        if expense_date and expense_date > end_date:
            raise serializers.ValidationError(
                {"expense_date": "Expense date cannot be after travel end date."}
            )

        if amount <= 0:
            raise serializers.ValidationError(
                {"amount": "Expense amount must be greater than 0."}
            )

        return attrs


class TravelExpenseListSerializer(BaseSerializer):
    travel_request = TravelRequestSimpleSerializer(read_only=True)
    amount_display = serializers.SerializerMethodField()

    class Meta:
        model = TravelExpense
        fields = (
            "id",
            "travel_request",
            "expense_date",
            "category",
            "amount",
            "description",
            "amount_display",
        )

    def get_amount_display(self, obj):
        return f"${obj.amount:,.2f}"


class TravelExpenseDetailSerializer(TravelExpenseSerializer):
    travel_request = TravelRequestSimpleSerializer(read_only=True)
    amount_display = serializers.SerializerMethodField()

    class Meta(TravelExpenseSerializer.Meta):
        fields = TravelExpenseSerializer.Meta.fields + ("amount_display",)

    def get_amount_display(self, obj):
        return f"${obj.amount:,.2f}"
