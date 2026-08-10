from django.db import transaction
from rest_framework.exceptions import ValidationError

from account.constants import AccountRole
from account.models.account import Account
from accounts_receivable.constants import InvoiceStatus
from accounts_receivable.models.sales_invoice import SalesInvoice
from accounts_receivable.models.sales_invoice_payment import SalesInvoicePayment
from journal.models.journal_entry import JournalEntry
from journal.models.journal_entry_line import JournalEntryLine
from sequence.services.sequence_service import SequenceService


class SalesInvoicePaymentService:

    @classmethod
    @transaction.atomic
    def create(
        cls,
        *,
        company,
        invoice,
        payment_date,
        amount,
        account,
        remarks,
    ):
        invoice = SalesInvoice.objects.select_for_update().get(pk=invoice.pk)

        paid_amount = sum(payment.amount for payment in invoice.payments.all())

        outstanding_amount = invoice.total - paid_amount

        if amount > outstanding_amount:
            raise ValidationError("Payment amount cannot exceed outstanding balance.")

        payment = SalesInvoicePayment.objects.create(
            company=company,
            invoice=invoice,
            payment_date=payment_date,
            amount=amount,
            account=account,
            remarks=remarks,
        )

        paid_amount += amount
        if paid_amount >= invoice.total:
            invoice.status = InvoiceStatus.PAID
            invoice.save(update_fields=["status"])

        journal_no = SequenceService.next(company=company, key="JOURNAL")
        journal = JournalEntry.objects.create(
            company=company,
            journal_no=journal_no,
            date=payment_date,
            description=f"Payment for {invoice.invoice_no}",
        )

        print("INVOICE COMPANY:", invoice.company_id)

        print(
            "ACCOUNTS:",
            list(
                Account.objects.filter(company=company).values(
                    "id",
                    "code",
                    "name",
                    "role",
                    "is_active",
                )
            ),
        )

        ar_account = Account.objects.get(
            company=company, role=AccountRole.ACCOUNTS_RECEIVABLE, is_active=True
        )

        JournalEntryLine.objects.create(
            journal=journal,
            account=account,
            description=f"Payment - {invoice.invoice_no}",
            debit=amount,
            credit=0,
        )

        JournalEntryLine.objects.create(
            journal=journal,
            account=ar_account,
            description=f"Accounts Receivable - {invoice.invoice_no}",
            debit=0,
            credit=amount,
        )

        payment.journal = journal
        payment.save(update_fields=["journal"])
        return payment
