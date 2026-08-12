from django.urls import include, path
from rest_framework import routers

from sales_order.views.sales_order_item_view_set import SalesOrderItemViewSet
from sales_order.views.sales_order_view_set import SalesOrderViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"sales-orders", SalesOrderViewSet)
router.register(r"sales-order-items", SalesOrderItemViewSet)

urlpatterns = [path("", include(router.urls))]
