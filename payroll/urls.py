from django.urls import include, path
from rest_framework import routers

from payroll.views.payroll_view_set import PayrollViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"payroll", PayrollViewSet)

urlpatterns = [path("", include(router.urls))]
