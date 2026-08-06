from django.urls import include, path
from rest_framework import routers

from company.views.company_view_set import CompanyViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"companies", CompanyViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
