from rest_framework import serializers

from attendance.models.attendance import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = [
            "id",
            "employee",
            "date",
            "check_in",
            "check_out",
            "status",
            "note",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "employee",
            "status",
            "created_at",
            "updated_at",
        ]


class AttendanceListSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()

    class Meta:
        model = Attendance
        fields = [
            "id",
            "employee",
            "employee_name",
            "date",
            "check_in",
            "check_out",
            "status",
        ]

    def get_employee_name(self, obj):
        return f"{obj.employee.first_name} {obj.employee.last_name}"


class AttendanceDetailSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()

    class Meta:
        model = Attendance
        fields = [
            "id",
            "employee",
            "employee_name",
            "date",
            "check_in",
            "check_out",
            "status",
            "note",
            "created_at",
            "updated_at",
        ]

    def get_employee_name(self, obj):
        return f"{obj.employee.first_name} {obj.employee.last_name}"


class AttendanceCheckInSerializer(serializers.Serializer):
    date = serializers.DateField()
    check_in = serializers.TimeField()


class AttendanceCheckOutSerializer(serializers.Serializer):
    date = serializers.DateField()
    check_out = serializers.TimeField()
