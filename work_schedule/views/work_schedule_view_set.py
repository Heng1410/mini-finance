from django_filters.rest_framework import DjangoFilterBackend

from base.views.company_base_view_set import CompanyBaseViewSet
from work_schedule.models.work_schedule import WorkSchedule
from work_schedule.serializers.work_schedule_serializer import (
    WorkScheduleDetailSerializer,
    WorkScheduleListSerializer,
    WorkScheduleSerializer,
)


class WorkScheduleViewSet(CompanyBaseViewSet):
    model = WorkSchedule
    queryset = WorkSchedule.objects.all()
    serializer_class = WorkScheduleSerializer

    filter_backends = CompanyBaseViewSet.filter_backends + (
        DjangoFilterBackend,
    )

    filterset_fields = {
        "is_active": ["exact"],
    }

    search_fields = [
        "name",
    ]

    def get_serializer_class(self):
        if self.action == "list":
            return WorkScheduleListSerializer

        if self.action == "retrieve":
            return WorkScheduleDetailSerializer

        return WorkScheduleSerializer