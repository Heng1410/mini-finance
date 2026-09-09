from datetime import datetime

from django.db import transaction

from attendance.constants import AttendanceStatus
from attendance.exception import (
    AlreadyCheckedOutException,
    AttendanceAlreadyExistsException,
    AttendanceNotFoundException,
    CheckInRequiredException,
    EmployeeOnLeaveException,
    InvalidCheckOutTimeException,
)
from attendance.models.attendance import Attendance
from leave.constants import LeaveRequestStatus
from leave.models.leave_request import LeaveRequest


class AttendanceService:

    @staticmethod
    def _has_approved_leave(employee, date):
        return LeaveRequest.objects.filter(
            company=employee.company,
            employee=employee,
            status=LeaveRequestStatus.APPROVED,
            start_date__lte=date,
            end_date__gte=date,
        ).exists()

    @staticmethod
    def _get_attendance_status(employee, date, check_in):
        work_schedule = employee.work_schedule

        if not work_schedule:
            return AttendanceStatus.PRESENT

        weekday = date.isoweekday()

        if weekday not in work_schedule.working_days:
            return AttendanceStatus.PRESENT

        if check_in > work_schedule.start_time:
            return AttendanceStatus.LATE

        return AttendanceStatus.PRESENT

    @staticmethod
    def _get_status_after_check_out(attendance):
        work_schedule = attendance.employee.work_schedule

        if not work_schedule:
            return attendance.status

        if attendance.date.isoweekday() not in work_schedule.working_days:
            return attendance.status

        check_in = datetime.combine(
            attendance.date,
            attendance.check_in,
        )
        check_out = datetime.combine(
            attendance.date,
            attendance.check_out,
        )

        schedule_start = datetime.combine(
            attendance.date,
            work_schedule.start_time,
        )
        schedule_end = datetime.combine(
            attendance.date,
            work_schedule.end_time,
        )
        work_duration = check_out - check_in
        schedule_duration = schedule_end - schedule_start
        
        if work_duration >= schedule_duration:
            return AttendanceStatus.PRESENT
        
        if work_duration < schedule_duration / 2:
            return AttendanceStatus.HALF_DAY

        return attendance.status

    @staticmethod
    @transaction.atomic
    def check_in(employee, date, check_in):
        if Attendance.objects.filter(
            company=employee.company,
            employee=employee,
            date=date,
        ).exists():
            raise AttendanceAlreadyExistsException()

        if AttendanceService._has_approved_leave(employee, date):
            raise EmployeeOnLeaveException()

        status = AttendanceService._get_attendance_status(
            employee=employee,
            date=date,
            check_in=check_in,
        )

        attendance = Attendance.objects.create(
            company=employee.company,
            employee=employee,
            date=date,
            check_in=check_in,
            status=status,
        )

        return attendance

    @staticmethod
    @transaction.atomic
    def check_out(employee, date, check_out):
        attendance = (
            Attendance.objects.select_for_update()
            .select_related("employee")
            .filter(company=employee.company, employee=employee, date=date)
            .first()
        )
        if not attendance:
            raise AttendanceNotFoundException()

        if not attendance.check_in:
            raise CheckInRequiredException()

        if attendance.check_out:
            raise AlreadyCheckedOutException()

        if check_out <= attendance.check_in:
            raise InvalidCheckOutTimeException()

        attendance.check_out = check_out
        attendance.status = AttendanceService._get_status_after_check_out(attendance)

        attendance.save(update_fields=["check_out", "updated_at", "status"])

        return attendance
