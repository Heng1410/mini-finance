from django.db.models import F, Sum
from account.constants import AccountType
from ledger.models.ledger_entry import LedgerEntry


class ProfitLossService:
    @classmethod
    def generate(cls, company):
        queryset = (
            LedgerEntry.objects.filter(company=company).values(
                code=F("account__code"),
                name=F("account__name"),
                account_type=F("account__account_type"),
            )
        ).annotate(debit=Sum("debit"), credit=Sum("credit"))

        groups = {AccountType.REVENUE: [], AccountType.EXPENSE: []}
        DEBIT_NORMAL = {
            AccountType.ASSET,
            AccountType.EXPENSE,
        }

        for row in queryset:
            account_type = row["account_type"]
            if account_type in DEBIT_NORMAL:
                row["balance"] = row["debit"] - row["credit"]
            else:
                row["balance"] = row["credit"] - row["debit"]

            if account_type in groups:
                groups[account_type].append(row)

        total_revenue = cls._calculate_total(groups[AccountType.REVENUE])
        total_expenses = cls._calculate_total(groups[AccountType.EXPENSE])
        net_profit = total_revenue - total_expenses

        return {
            "revenue": groups[AccountType.REVENUE],
            "expenses": groups[AccountType.EXPENSE],
            "total_revenue": total_revenue,
            "total_expenses": total_expenses,
            "net_profit": net_profit,
        }

    @staticmethod
    def _calculate_total(items):
        return sum(item["balance"] for item in items)
