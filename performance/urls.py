from django.urls import include, path
from rest_framework import routers

from performance.views.performance_view_set import PerformanceReviewViewSet


router = routers.DefaultRouter(trailing_slash=False)
router.register(r"performance-review", PerformanceReviewViewSet)

urlpatterns = [path("", include(router.urls))]
