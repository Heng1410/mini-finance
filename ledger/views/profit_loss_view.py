from rest_framework.views import APIView
from rest_framework.response import Response

from ledger.serializers.profit_loss_serializer import ProfitLossSerializer
from ledger.services.profit_loss_service import ProfitLossService


class ProfitLossView(APIView):

    def get(self, request):
        result = ProfitLossService.generate(request.user.employee.company)
        serializer = ProfitLossSerializer(result)

        return Response(serializer.data)
