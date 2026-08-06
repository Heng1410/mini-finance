from django.urls import include, path
from rest_framework import routers

from employee.views.employee_view_set import EmployeeViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"employees", EmployeeViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
