from django.urls import include, path
from rest_framework import routers

from work_schedule.views.work_schedule_view_set import WorkScheduleViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"work_schedule", WorkScheduleViewSet)

urlpatterns = [path("", include(router.urls))]
