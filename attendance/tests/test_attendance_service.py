from datetime import date, time

from django.test import TestCase

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
from attendance.services.attendance_service import AttendanceService
from company.models.company import Company
from department.models.department import Department
from employee.models.employee import Employee
from leave.constants import LeaveRequestStatus
from leave.models.leave_request import LeaveRequest
from leave.models.leave_type import LeaveType
from role.models.role import Role


class AttendanceServiceTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.company = Company.objects.create(
            name="Test Company",
            code="TEST",
            legal_name="Test Company Ltd.",
            registration_number="REG-TEST-001",
            tax_number="TAX-TEST-001",
            country="Cambodia",
            currency="USD",
            timezone="Asia/Phnom_Penh",
            fiscal_year_start=date(2026, 1, 1),
        )

        cls.department = Department.objects.create(
            company=cls.company,
            name="Human Resources",
            code="HR",
        )

        cls.role = Role.objects.create(
            company=cls.company,
            name="Employee",
            code="EMP",
        )

        cls.employee = Employee.objects.create(
            company=cls.company,
            department=cls.department,
            role=cls.role,
            employee_code="EMP001",
            first_name="John",
            last_name="Doe",
            email="john@test.com",
            phone="012345678",
            hire_date=date(2026, 1, 1),
            job_title="Software Developer",
        )

        cls.leave_type = LeaveType.objects.create(
            company=cls.company,
            code="ANNUAL",
            name="Annual Leave",
            days_per_year=18,
            is_active=True,
        )

    def create_attendance(
        self,
        attendance_date=date(2026, 9, 9),
        check_in=time(8, 0),
        check_out=None,
    ):
        return Attendance.objects.create(
            company=self.company,
            employee=self.employee,
            date=attendance_date,
            check_in=check_in,
            check_out=check_out,
            status=AttendanceStatus.PRESENT,
        )

    # CHECK IN

    def test_check_in_success(self):
        attendance = AttendanceService.check_in(
            employee=self.employee,
            date=date(2026, 9, 9),
            check_in=time(8, 0),
        )

        self.assertEqual(attendance.employee, self.employee)
        self.assertEqual(attendance.date, date(2026, 9, 9))
        self.assertEqual(attendance.check_in, time(8, 0))
        self.assertEqual(attendance.status, AttendanceStatus.PRESENT)

    def test_check_in_duplicate_fails(self):
        self.create_attendance()

        with self.assertRaises(AttendanceAlreadyExistsException):
            AttendanceService.check_in(
                employee=self.employee,
                date=date(2026, 9, 9),
                check_in=time(8, 30),
            )

    def test_check_in_on_approved_leave_fails(self):
        LeaveRequest.objects.create(
            company=self.company,
            employee=self.employee,
            leave_type=self.leave_type,
            start_date=date(2026, 9, 9),
            end_date=date(2026, 9, 9),
            status=LeaveRequestStatus.APPROVED,
        )

        with self.assertRaises(EmployeeOnLeaveException):
            AttendanceService.check_in(
                employee=self.employee,
                date=date(2026, 9, 9),
                check_in=time(8, 0),
            )

    # CHECK OUT

    def test_check_out_success(self):
        self.create_attendance(
            check_in=time(8, 0),
        )

        attendance = AttendanceService.check_out(
            employee=self.employee,
            date=date(2026, 9, 9),
            check_out=time(17, 0),
        )

        self.assertEqual(attendance.check_out, time(17, 0))

    def test_check_out_without_attendance_fails(self):
        with self.assertRaises(AttendanceNotFoundException):
            AttendanceService.check_out(
                employee=self.employee,
                date=date(2026, 9, 9),
                check_out=time(17, 0),
            )

    def test_check_out_without_check_in_fails(self):
        self.create_attendance(check_in=None)

        with self.assertRaises(CheckInRequiredException):
            AttendanceService.check_out(
                employee=self.employee,
                date=date(2026, 9, 9),
                check_out=time(17, 0),
            )

    def test_check_out_twice_fails(self):
        self.create_attendance(
            check_in=time(8, 0),
            check_out=time(17, 0),
        )

        with self.assertRaises(AlreadyCheckedOutException):
            AttendanceService.check_out(
                employee=self.employee,
                date=date(2026, 9, 9),
                check_out=time(18, 0),
            )

    def test_check_out_before_check_in_fails(self):
        self.create_attendance(
            check_in=time(8, 0),
        )

        with self.assertRaises(InvalidCheckOutTimeException):
            AttendanceService.check_out(
                employee=self.employee,
                date=date(2026, 9, 9),
                check_out=time(7, 59),
            )

    # COMPANY ISOLATION

    def test_cannot_check_out_attendance_from_another_company(self):
        other_company = Company.objects.create(
            name="Other Company",
            code="OTHER",
            legal_name="Other Company Ltd.",
            registration_number="REG-OTHER-001",
            tax_number="TAX-OTHER-001",
            country="Cambodia",
            currency="USD",
            timezone="Asia/Phnom_Penh",
            fiscal_year_start=date(2026, 1, 1),
        )

        attendance = Attendance.objects.create(
            company=other_company,
            employee=self.employee,
            date=date(2026, 9, 9),
            check_in=time(8, 0),
            status=AttendanceStatus.PRESENT,
        )

        with self.assertRaises(AttendanceNotFoundException):
            AttendanceService.check_out(
                employee=self.employee,
                date=attendance.date,
                check_out=time(17, 0),
            )