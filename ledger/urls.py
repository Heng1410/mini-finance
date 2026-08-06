from django.urls import path, include
from rest_framework import routers

from ledger.views.balance_sheet_view import BalanceSheetView
from ledger.views.general_ledger_view import GeneralLedgerView
from ledger.views.profit_loss_view import ProfitLossView
from ledger.views.trial_balance_view import TrialBalanceView

router = routers.DefaultRouter(trailing_slash=False)

urlpatterns = [
    path(
        "general-ledger",
        GeneralLedgerView.as_view(),
        name="general-ledger",
    ),
    path(
        "trial-balance",
        TrialBalanceView.as_view(),
        name="trial-balance",
    ),
    path("balance-sheet", BalanceSheetView.as_view(), name="balance-sheet"),
    path("profit-loss", ProfitLossView.as_view(), name="profit-loss"),
    path("", include(router.urls)),
]
