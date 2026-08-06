from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from ledger.models.ledger_entry import LedgerEntry
from ledger.serializers.general_ledger_serializer import GeneralLedgerSerializer


class GeneralLedgerView(APIView):

    def get(self, request):
        account = request.query_params.get("account")
        if not account:
            raise ValidationError({"account": ["This query parameter is required."]})

        queryset = (
            LedgerEntry.objects.filter(
                company=request.user.employee.company, account_id=account
            ).select_related("journal")
        ).order_by("date", "id")

        balance = 0

        result = []

        for row in queryset:
            balance += row.debit
            balance -= row.credit

            result.append(
                {
                    "date": row.date,
                    "journal_no": row.journal.journal_no,
                    "description": row.description,
                    "debit": row.debit,
                    "credit": row.credit,
                    "balance": balance,
                }
            )

        serializer = GeneralLedgerSerializer(result, many=True)

        return Response(serializer.data)
