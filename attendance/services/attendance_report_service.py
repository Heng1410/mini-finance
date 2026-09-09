from django.db.models import Q
from django.db.models.aggregates import Count

from attendance.constants import AttendanceStatus
from attendance.models.attendance import Attendance


class AttendanceReportService:

    @staticmethod
    def get_summary(employee, start_date, end_date):
        attendance = Attendance.objects.filter(
            company=employee.company,
            employee=employee,
            date__gte=start_date,
            date__lte=end_date,
        )

        summary = attendance.aggregate(
            total_days=Count("id"),
            present_days=Count("id", filter=Q(status=AttendanceStatus.PRESENT)),
            late_days=Count("id", filter=Q(status=AttendanceStatus.LATE)),
            half_days=Count(
                "id",
                filter=Q(status=AttendanceStatus.HALF_DAY),
            ),
            absent_days=Count(
                "id",
                filter=Q(status=AttendanceStatus.ABSENT),
            ),
            leave_days=Count(
                "id",
                filter=Q(status=AttendanceStatus.ON_LEAVE),
            ),
        )

        return {
            "employee": employee.id,
            "start_date": start_date,
            "end_date": end_date,
            **summary,
        }
