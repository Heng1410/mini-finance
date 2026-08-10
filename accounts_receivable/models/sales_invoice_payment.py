from django.db import models

from account.models.account import Account
from accounts_receivable.models.sales_invoice import SalesInvoice
from base.models.company_base_model import CompanyBaseModel
from journal.models.journal_entry import JournalEntry


class SalesInvoicePayment(CompanyBaseModel):
    invoice = models.ForeignKey(
        SalesInvoice, on_delete=models.PROTECT, related_name="payments"
    )

    payment_date = models.DateField()

    amount = models.DecimalField(max_digits=18, decimal_places=2)

    account = models.ForeignKey(
        Account, on_delete=models.PROTECT, related_name="sales_invoice_payments"
    )

    journal = models.OneToOneField(
        JournalEntry,
        on_delete=models.PROTECT,
        related_name="sales_invoice_payment",
        blank=True,
        null=True,
    )

    remarks = models.TextField(blank=True)

    class Meta:
        db_table = "sales_invoice_payments"
