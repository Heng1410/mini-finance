from django.db.models import DecimalField, F, Value
from django.db.models.aggregates import Sum
from django.db.models.functions import Coalesce

from accounts_receivable.constants import InvoiceStatus
from accounts_receivable.models.sales_invoice import SalesInvoice
from accounts_receivable.models.sales_invoice_payment import SalesInvoicePayment


class CustomerOutstandingInvoicesService:
    @classmethod
    def get_outstanding_invoice(cls, *, customer):
        invoices = (
            SalesInvoice.objects.filter(customer=customer)
            .exclude(status=InvoiceStatus.DRAFT)
            .annotate(
                paid=Coalesce(
                    Sum("payments__amount"),
                    Value(
                        0,
                        output_field=DecimalField(
                            max_digits=18,
                            decimal_places=2,
                        ),
                    ),
                )
            )
            .annotate(outstanding=F("total") - F("paid"))
            .filter(outstanding__gt=0)
        )
        return invoices
