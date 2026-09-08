from datetime import date
from decimal import Decimal

from django.test import TestCase

from company.models.company import Company
from department.models.department import Department
from employee.models.employee import Employee
from leave.constants import LeaveRequestStatus
from leave.exception import (
    InsufficientLeaveBalanceException,
    LeaveRequestNotPendingException,
    LeaveRequestStatusException,
)
from leave.models.leave_balance import LeaveBalance
from leave.models.leave_request import LeaveRequest
from leave.models.leave_type import LeaveType
from leave.services.leave_request_service import LeaveRequestService
from role.models.role import Role


class LeaveRequestServiceTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # ---------------------------------------------------------
        # COMPANY
        # ---------------------------------------------------------

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

        # ---------------------------------------------------------
        # DEPARTMENT
        # ---------------------------------------------------------

        cls.department = Department.objects.create(
            company=cls.company,
            name="Human Resources",
            code="HR",
        )

        # ---------------------------------------------------------
        # ROLE
        # ---------------------------------------------------------

        cls.role = Role.objects.create(
            company=cls.company,
            name="Employee",
            code="EMP",
        )

        # ---------------------------------------------------------
        # EMPLOYEE
        # ---------------------------------------------------------

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

        # ---------------------------------------------------------
        # LEAVE TYPE
        # ---------------------------------------------------------

        cls.leave_type = LeaveType.objects.create(
            company=cls.company,
            code="ANNUAL",
            name="Annual Leave",
            days_per_year=Decimal("18.00"),
            is_active=True,
        )

    def setUp(self):
        # Each test gets a fresh balance.
        self.balance = LeaveBalance.objects.create(
            company=self.company,
            employee=self.employee,
            leave_type=self.leave_type,
            year=2026,
            allocated_days=Decimal("18.00"),
            used_days=Decimal("0.00"),
        )

    def create_request(
        self,
        start_date=date(2026, 9, 10),
        end_date=date(2026, 9, 12),
        status=LeaveRequestStatus.PENDING,
        reason="Family trip",
    ):
        return LeaveRequest.objects.create(
            company=self.company,
            employee=self.employee,
            leave_type=self.leave_type,
            start_date=start_date,
            end_date=end_date,
            reason=reason,
            status=status,
        )

    # =========================================================
    # APPROVE
    # =========================================================

    def test_approve_pending_leave(self):
        leave_request = self.create_request()

        result = LeaveRequestService.approve(
            leave_request.id,
            self.company,
        )

        leave_request.refresh_from_db()
        self.balance.refresh_from_db()

        self.assertEqual(
            result.status,
            LeaveRequestStatus.APPROVED,
        )

        self.assertEqual(
            leave_request.status,
            LeaveRequestStatus.APPROVED,
        )

        # Sep 10 -> Sep 12 = 3 days
        self.assertEqual(
            self.balance.used_days,
            Decimal("3.00"),
        )

    def test_approve_already_approved_leave_fails(self):
        leave_request = self.create_request(
            status=LeaveRequestStatus.APPROVED,
        )

        with self.assertRaises(LeaveRequestStatusException):
            LeaveRequestService.approve(
                leave_request.id,
                self.company,
            )

    def test_approve_rejected_leave_fails(self):
        leave_request = self.create_request(
            status=LeaveRequestStatus.REJECTED,
        )

        with self.assertRaises(LeaveRequestStatusException):
            LeaveRequestService.approve(
                leave_request.id,
                self.company,
            )

    def test_approve_cancelled_leave_fails(self):
        leave_request = self.create_request(
            status=LeaveRequestStatus.CANCELLED,
        )

        with self.assertRaises(LeaveRequestStatusException):
            LeaveRequestService.approve(
                leave_request.id,
                self.company,
            )

    def test_approve_insufficient_balance_fails(self):
        leave_request = self.create_request(
            start_date=date(2026, 9, 10),
            end_date=date(2026, 9, 28),
        )

        with self.assertRaises(InsufficientLeaveBalanceException):
            LeaveRequestService.approve(
                leave_request.id,
                self.company,
            )

        leave_request.refresh_from_db()
        self.balance.refresh_from_db()

        # Transaction must roll back the status change.
        self.assertEqual(
            leave_request.status,
            LeaveRequestStatus.PENDING,
        )

        # Balance must also remain unchanged.
        self.assertEqual(
            self.balance.used_days,
            Decimal("0.00"),
        )

    def test_approve_overlapping_leave_fails(self):
        # First request
        first_request = self.create_request(
            start_date=date(2026, 9, 10),
            end_date=date(2026, 9, 12),
        )

        LeaveRequestService.approve(
            first_request.id,
            self.company,
        )

        # Second request overlaps Sep 11-12.
        second_request = self.create_request(
            start_date=date(2026, 9, 11),
            end_date=date(2026, 9, 15),
        )

        with self.assertRaises(LeaveRequestStatusException):
            LeaveRequestService.approve(
                second_request.id,
                self.company,
            )

        second_request.refresh_from_db()
        self.balance.refresh_from_db()

        # Second request must stay pending.
        self.assertEqual(
            second_request.status,
            LeaveRequestStatus.PENDING,
        )

        # Only first request consumed balance.
        self.assertEqual(
            self.balance.used_days,
            Decimal("3.00"),
        )

    def test_approve_adjacent_leave_is_allowed(self):
        # First: Sep 10-12
        first_request = self.create_request(
            start_date=date(2026, 9, 10),
            end_date=date(2026, 9, 12),
        )

        LeaveRequestService.approve(
            first_request.id,
            self.company,
        )

        # Second starts immediately after.
        # Sep 13-15 does NOT overlap.
        second_request = self.create_request(
            start_date=date(2026, 9, 13),
            end_date=date(2026, 9, 15),
        )

        LeaveRequestService.approve(
            second_request.id,
            self.company,
        )

        second_request.refresh_from_db()
        self.balance.refresh_from_db()

        self.assertEqual(
            second_request.status,
            LeaveRequestStatus.APPROVED,
        )

        # 3 + 3 = 6 days
        self.assertEqual(
            self.balance.used_days,
            Decimal("6.00"),
        )

    # =========================================================
    # REJECT
    # =========================================================

    def test_reject_pending_leave(self):
        leave_request = self.create_request()

        result = LeaveRequestService.reject(
            leave_request.id,
            self.company,
        )

        leave_request.refresh_from_db()

        self.assertEqual(
            result.status,
            LeaveRequestStatus.REJECTED,
        )

        self.assertEqual(
            leave_request.status,
            LeaveRequestStatus.REJECTED,
        )

    def test_reject_approved_leave_fails(self):
        leave_request = self.create_request(
            status=LeaveRequestStatus.APPROVED,
        )

        with self.assertRaises(LeaveRequestNotPendingException):
            LeaveRequestService.reject(
                leave_request.id,
                self.company,
            )

    def test_reject_cancelled_leave_fails(self):
        leave_request = self.create_request(
            status=LeaveRequestStatus.CANCELLED,
        )

        with self.assertRaises(LeaveRequestNotPendingException):
            LeaveRequestService.reject(
                leave_request.id,
                self.company,
            )

    def test_reject_already_rejected_leave_fails(self):
        leave_request = self.create_request(
            status=LeaveRequestStatus.REJECTED,
        )

        with self.assertRaises(LeaveRequestNotPendingException):
            LeaveRequestService.reject(
                leave_request.id,
                self.company,
            )

    # =========================================================
    # CANCEL
    # =========================================================

    def test_cancel_pending_leave(self):
        leave_request = self.create_request()

        result = LeaveRequestService.cancel(
            leave_request.id,
            self.company,
        )

        leave_request.refresh_from_db()
        self.balance.refresh_from_db()

        self.assertEqual(
            result.status,
            LeaveRequestStatus.CANCELLED,
        )

        self.assertEqual(
            leave_request.status,
            LeaveRequestStatus.CANCELLED,
        )

        # Pending leave never consumed balance.
        self.assertEqual(
            self.balance.used_days,
            Decimal("0.00"),
        )

    def test_cancel_approved_leave_restores_balance(self):
        leave_request = self.create_request()

        # Approve first.
        LeaveRequestService.approve(
            leave_request.id,
            self.company,
        )

        self.balance.refresh_from_db()

        self.assertEqual(
            self.balance.used_days,
            Decimal("3.00"),
        )

        # Then cancel.
        LeaveRequestService.cancel(
            leave_request.id,
            self.company,
        )

        leave_request.refresh_from_db()
        self.balance.refresh_from_db()

        self.assertEqual(
            leave_request.status,
            LeaveRequestStatus.CANCELLED,
        )

        # The 3 approved days must be returned.
        self.assertEqual(
            self.balance.used_days,
            Decimal("0.00"),
        )

    def test_cancel_rejected_leave_fails(self):
        leave_request = self.create_request(
            status=LeaveRequestStatus.REJECTED,
        )

        with self.assertRaises(LeaveRequestStatusException):
            LeaveRequestService.cancel(
                leave_request.id,
                self.company,
            )

    def test_cancel_already_cancelled_leave_fails(self):
        leave_request = self.create_request(
            status=LeaveRequestStatus.CANCELLED,
        )

        with self.assertRaises(LeaveRequestStatusException):
            LeaveRequestService.cancel(
                leave_request.id,
                self.company,
            )

    # =========================================================
    # LEAVE DAY CALCULATION / BALANCE
    # =========================================================

    def test_approve_one_day_leave(self):
        leave_request = self.create_request(
            start_date=date(2026, 9, 10),
            end_date=date(2026, 9, 10),
        )

        LeaveRequestService.approve(
            leave_request.id,
            self.company,
        )

        self.balance.refresh_from_db()

        self.assertEqual(
            self.balance.used_days,
            Decimal("1.00"),
        )

    def test_approve_multiple_leave_requests_updates_balance(self):
        # First leave = 3 days
        first_request = self.create_request(
            start_date=date(2026, 9, 10),
            end_date=date(2026, 9, 12),
        )

        LeaveRequestService.approve(
            first_request.id,
            self.company,
        )

        # Second leave = 5 days
        second_request = self.create_request(
            start_date=date(2026, 9, 15),
            end_date=date(2026, 9, 19),
        )

        LeaveRequestService.approve(
            second_request.id,
            self.company,
        )

        self.balance.refresh_from_db()

        # 3 + 5 = 8
        self.assertEqual(
            self.balance.used_days,
            Decimal("8.00"),
        )

        # 18 - 8 = 10
        self.assertEqual(
            self.balance.allocated_days
            - self.balance.used_days,
            Decimal("10.00"),
        )

    # =========================================================
    # COMPANY ISOLATION
    # =========================================================

    def test_cannot_approve_leave_from_another_company(self):
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

        leave_request = LeaveRequest.objects.create(
            company=other_company,
            employee=self.employee,
            leave_type=self.leave_type,
            start_date=date(2026, 9, 10),
            end_date=date(2026, 9, 12),
            reason="Other company request",
            status=LeaveRequestStatus.PENDING,
        )

        with self.assertRaises(LeaveRequest.DoesNotExist):
            LeaveRequestService.approve(
                leave_request.id,
                self.company,
            )