from rest_framework import serializers

from work_schedule.models.work_schedule import WorkSchedule


class WorkScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSchedule
        fields = [
            "id",
            "name",
            "start_time",
            "end_time",
            "working_days",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class WorkScheduleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSchedule
        fields = [
            "id",
            "name",
            "start_time",
            "end_time",
            "working_days",
            "is_active",
        ]


class WorkScheduleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSchedule
        fields = [
            "id",
            "name",
            "start_time",
            "end_time",
            "working_days",
            "is_active",
            "created_at",
            "updated_at",
        ]