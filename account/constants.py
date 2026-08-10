from django.db import models


class AccountType(models.TextChoices):
    ASSET = "ASSET", "Asset"
    LIABILITY = "LIABILITY", "Liability"
    EQUITY = "EQUITY", "Equity"
    REVENUE = "REVENUE", "Revenue"
    EXPENSE = "EXPENSE", "Expense"


class AccountRole(models.TextChoices):
    ACCOUNTS_RECEIVABLE = "ACCOUNTS_RECEIVABLE", "Accounts Receivable"
    SALES_REVENUE = "SALES_REVENUE", "Sales Revenue"
