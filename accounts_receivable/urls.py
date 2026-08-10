from django.urls import include, path
from rest_framework import routers

from accounts_receivable.views.customer_view_set import CustomerViewSet
from accounts_receivable.views.sales_invoice_payment_view_set import (
    SalesInvoicePaymentViewSet,
)
from accounts_receivable.views.sales_invoice_view_set import SalesInvoiceViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"customers", CustomerViewSet)
router.register(r"sales-invoice", SalesInvoiceViewSet)
router.register(r"sales-invoice-payments", SalesInvoicePaymentViewSet)

urlpatterns = [path("", include(router.urls))]
