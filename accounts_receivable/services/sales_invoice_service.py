from rest_framework.exceptions import ValidationError
from django.db import transaction

from account.constants import AccountRole
from account.models.account import Account
from accounts_receivable.constants import InvoiceStatus
from accounts_receivable.models.sales_invoice import SalesInvoice
from accounts_receivable.models.sales_invoice_line import SalesInvoiceLine
from journal.models.journal_entry_line import JournalEntryLine
from sequence.services.sequence_service import SequenceService
from journal.models.journal_entry import JournalEntry


class SalesInvoiceService:
    @classmethod
    @transaction.atomic
    def create(cls, *, company, customer, invoice_date, due_date, remarks, lines):
        if due_date < invoice_date:
            raise ValidationError(
                "Due date must be greater than or equal to invoice date."
            )

        if not lines:
            raise ValidationError("Line must be provided")

        invoice_no = SequenceService.next(company=company, key="SALES_INVOICE")

        invoice = SalesInvoice.objects.create(
            company=company,
            customer=customer,
            invoice_date=invoice_date,
            invoice_no=invoice_no,
            due_date=due_date,
            remarks=remarks,
        )
        invoice_total = 0
        for line in lines:
            description = line["description"]
            quantity = line["quantity"]
            unit_price = line["unit_price"]
            line_total = quantity * unit_price
            SalesInvoiceLine.objects.create(
                sales_invoice=invoice,
                description=description,
                quantity=quantity,
                unit_price=unit_price,
                line_total=line_total,
            )
            invoice_total += line_total

        invoice.total = invoice_total
        invoice.save(update_fields=["total"])
        return invoice

    @classmethod
    @transaction.atomic
    def approve(cls, *, invoice):

        invoice = SalesInvoice.objects.select_for_update().get(pk=invoice.pk)

        if invoice.status != InvoiceStatus.DRAFT:
            raise ValidationError("Only draft invoices can be approved.")

        if invoice.total <= 0:
            raise ValidationError("Invoice total must be greater than zero.")

        company = invoice.company

        ar_account = Account.objects.get(
            company=company, role=AccountRole.ACCOUNTS_RECEIVABLE, is_active=True
        )

        revenue_account = Account.objects.get(
            company=company, role=AccountRole.SALES_REVENUE, is_active=True
        )

        journal_no = SequenceService.next(company=company, key="JOURNAL")

        journal = JournalEntry.objects.create(
            company=company,
            journal_no=journal_no,
            date=invoice.invoice_date,
            description=f"Sales Invoice {invoice.invoice_no}",
        )

        JournalEntryLine.objects.create(
            journal=journal,
            account=ar_account,
            description=f"Accounts Receivable - {invoice.invoice_no}",
            debit=invoice.total,
            credit=0,
        )

        JournalEntryLine.objects.create(
            journal=journal,
            account=revenue_account,
            description=f"Sales Revenue - {invoice.invoice_no}",
            debit=0,
            credit=invoice.total,
        )

        invoice.journal = journal
        invoice.status = InvoiceStatus.APPROVED
        invoice.save(update_fields=["status", "journal"])

        return invoice
