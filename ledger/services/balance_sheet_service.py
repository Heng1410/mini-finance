from django.db.models import F, Sum

from account.constants import AccountType
from ledger.models.ledger_entry import LedgerEntry


class BalanceSheetService:
    @classmethod
    def generate(cls, company):
        queryset = (
            LedgerEntry.objects.filter(company=company)
            .values(
                code=F("account__code"),
                name=F("account__name"),
                account_type=F("account__account_type"),
            )
            .annotate(balance=Sum("debit") - Sum("credit"))
        )
        groups = {
            AccountType.ASSET: [],
            AccountType.LIABILITY: [],
            AccountType.EQUITY: [],
        }

        for row in queryset:
            account_type = row["account_type"]

            if account_type in groups:
                groups[account_type].append(row)
                
        def calculate_total(items):
            return sum(item["balance"] for item in items)

        total_assets = calculate_total(groups[AccountType.ASSET])       
        total_liabilities = calculate_total(groups[AccountType.LIABILITY])
        total_equity = calculate_total(groups[AccountType.EQUITY])

        return {
            "assets": groups[AccountType.ASSET],
            "liabilities": groups[AccountType.LIABILITY],
            "equity": groups[AccountType.EQUITY],
            "total_assets": total_assets,
            "total_liabilities": total_liabilities,
            "total_equity": total_equity,
        }
