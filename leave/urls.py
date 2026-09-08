from rest_framework.routers import DefaultRouter
from django.urls import include, path

from leave.views.leave_balance_view_set import LeaveBalanceViewSet
from leave.views.leave_request_view_set import LeaveRequestViewSet
from leave.views.leave_type_view_set import LeaveTypeViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"leave_type", LeaveTypeViewSet)
router.register(r"leave_request", LeaveRequestViewSet)
router.register(r"leave_balance", LeaveBalanceViewSet)

urlpatterns = [path("", include(router.urls))]
