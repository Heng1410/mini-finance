from rest_framework.views import APIView
from rest_framework.response import Response

from ledger.serializers.balance_sheet_serializer import BalanceSheetSerializer
from ledger.services.balance_sheet_service import BalanceSheetService


class BalanceSheetView(APIView):
    def get(self, request):

        result = BalanceSheetService.generate(request.user.employee.company)

        serializer = BalanceSheetSerializer(result)

        return Response(serializer.data)
