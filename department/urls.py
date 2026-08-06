from django.urls import include,path 
from rest_framework import routers

from department.views.department_view_set import DepartmentViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"departments", DepartmentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]