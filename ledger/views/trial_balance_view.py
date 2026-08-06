from django.db.models import F, Sum
from rest_framework.response import Response
from rest_framework.views import APIView

from ledger.models.ledger_entry import LedgerEntry
from ledger.serializers.trial_balance_serializer import TrialBalanceSerializer


class TrialBalanceView(APIView):
    def get(self, request):
        queryset = (
            LedgerEntry.objects.filter(company=request.user.employee.company)
            .values(code=F("account__code"), name=F("account__name"))
            .annotate(debit=Sum("debit"), credit=Sum("credit"))
            .order_by("code")
        )

        serializer = TrialBalanceSerializer(queryset, many=True)

        return Response(serializer.data)
