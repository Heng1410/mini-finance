from rest_framework import status
from rest_framework.exceptions import APIException


class AttendanceException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST


class AttendanceAlreadyExistsException(AttendanceException):
    default_detail = (
        "Attendance record already exists for this employee and date."
    )


class AttendanceNotFoundException(AttendanceException):
    default_detail = "Attendance record does not exist."


class EmployeeOnLeaveException(AttendanceException):
    default_detail = "Employee is on approved leave for this date."


class CheckInRequiredException(AttendanceException):
    default_detail = "Employee must check in before checking out."


class AlreadyCheckedOutException(AttendanceException):
    default_detail = "Employee has already checked out."


class InvalidCheckOutTimeException(AttendanceException):
    default_detail = "Check-out time must be later than check-in time."