from django.db import transaction

from leave.constants import LeaveRequestStatus
from leave.exception import LeaveRequestNotPendingException, LeaveRequestStatusException
from leave.models.leave_request import LeaveRequest
from leave.services.leave_balance_service import LeaveBalanceService
from leave.utils.leave_date_utils import calculate_leave_days


class LeaveRequestService:

    @staticmethod
    def _get_locked_leave_request(leave_request_id, company):
        return (
            LeaveRequest.objects.select_for_update()
            .select_related("employee", "leave_type")
            .get(
                id=leave_request_id,
                company=company,
            )
        )

    @staticmethod
    @transaction.atomic
    def approve(leave_request_id, company):
        leave_request = LeaveRequestService._get_locked_leave_request(
            leave_request_id,
            company,
        )

        if leave_request.status != LeaveRequestStatus.PENDING:
            raise LeaveRequestStatusException(
                "Only pending leave requests can be approved."
            )

        if LeaveRequestService._has_overlapping_approved_leave(leave_request):
            raise LeaveRequestStatusException(
                "Employee already has an approved leave request "
                "that overlaps this period."
            )

        days = calculate_leave_days(leave_request.start_date, leave_request.end_date)

        balance = LeaveBalanceService.get_balance(
            employee=leave_request.employee,
            leave_type=leave_request.leave_type,
            year=leave_request.start_date.year,
        )

        LeaveBalanceService.add_used_days(balance=balance, days=days)

        leave_request.status = LeaveRequestStatus.APPROVED
        leave_request.save(update_fields=["status", "updated_at"])

        return leave_request

    @staticmethod
    @transaction.atomic
    def reject(leave_request_id, company):
        leave_request = LeaveRequestService._get_locked_leave_request(
            leave_request_id,
            company,
        )

        if leave_request.status != LeaveRequestStatus.PENDING:
            raise LeaveRequestNotPendingException()

        leave_request.status = LeaveRequestStatus.REJECTED
        leave_request.save(update_fields=["status", "updated_at"])

        return leave_request

    @staticmethod
    @transaction.atomic
    def cancel(leave_request_id, company):
        leave_request = LeaveRequestService._get_locked_leave_request(
            leave_request_id, company
        )

        if leave_request.status not in (
            LeaveRequestStatus.PENDING,
            LeaveRequestStatus.APPROVED,
        ):
            raise LeaveRequestStatusException(
                "Only pending or approved leave requests can be cancelled."
            )

        if leave_request.status == LeaveRequestStatus.APPROVED:
            days = calculate_leave_days(
                leave_request.start_date,
                leave_request.end_date,
            )

            balance = LeaveBalanceService.get_balance(
                employee=leave_request.employee,
                leave_type=leave_request.leave_type,
                year=leave_request.start_date.year,
            )

            LeaveBalanceService.subtract_used_days(balance=balance, days=days)

        leave_request.status = LeaveRequestStatus.CANCELLED
        leave_request.save(update_fields=["status", "updated_at"])

        return leave_request

    @staticmethod
    def _has_overlapping_approved_leave(leave_request):
        return (
            LeaveRequest.objects.filter(
                company=leave_request.company,
                employee=leave_request.employee,
                status=LeaveRequestStatus.APPROVED,
                start_date__lte=leave_request.end_date,
                end_date__gte=leave_request.start_date,
            )
            .exclude(
                id=leave_request.id,
            )
            .exists()
        )
