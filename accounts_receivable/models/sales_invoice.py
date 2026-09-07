from django.db import models

from accounts_receivable.constants import InvoiceStatus
from accounts_receivable.models.customer import Customer
from base.models.company_base_model import CompanyBaseModel
from delivery.models.delivery import Delivery
from journal.models.journal_entry import JournalEntry


class SalesInvoice(CompanyBaseModel):
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, related_name="sales_invoices"
    )
    invoice_no = models.CharField(max_length=32)
    invoice_date = models.DateField()
    journal = models.OneToOneField(
        JournalEntry,
        on_delete=models.PROTECT,
        related_name="sales_invoice",
        null=True,
        blank=True,
    )
    delivery = models.OneToOneField(
        Delivery,
        on_delete=models.PROTECT,
        related_name="invoice",
        null=True,
        blank=True,
    )
    due_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=InvoiceStatus.choices,
        default=InvoiceStatus.DRAFT,
        db_index=True,
    )
    remarks = models.TextField(blank=True)
    total = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    class Meta:
        db_table = "sales_invoices"
        ordering = ("-invoice_date", "-id")
        constraints = [
            models.UniqueConstraint(
                fields=["company", "invoice_no"], name="uq_invoice_no_per_company"
            )
        ]
