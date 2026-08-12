from django.urls import include, path
from rest_framework import routers

from case_support.views.case_view_set import CaseViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"cases", CaseViewSet)

urlpatterns = [path("", include(router.urls))]
