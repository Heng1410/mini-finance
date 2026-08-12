from django.db import transaction
from django.db.models.aggregates import Sum

from accounts_receivable.constants import InvoiceStatus
from accounts_receivable.models.sales_invoice import SalesInvoice
from accounts_receivable.models.sales_invoice_payment import SalesInvoicePayment


class CustomerInvoiceSummaryService:
    @classmethod
    def get_summary(cls, *, customer):
        invoices = SalesInvoice.objects.filter(customer=customer).exclude(
            status=InvoiceStatus.DRAFT
        )
        invoice_count = invoices.count()
        total_invoiced = invoices.aggregate(total=Sum("total"))["total"] or 0
        total_paid = (
            SalesInvoicePayment.objects.filter(invoice__in=invoices).aggregate(
                total=Sum("amount")
            )["total"]
            or 0
        )
        total_outstanding = total_invoiced - total_paid

        return {
            "total_invoices": invoice_count,
            "total_invoiced": total_invoiced,
            "total_paid": total_paid,
            "total_outstanding": total_outstanding,
        }
