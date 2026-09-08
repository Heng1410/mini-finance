from decimal import Decimal

from django.db import transaction

from leave.exception import (
    InsufficientLeaveBalanceException,
    InvalidLeaveBalanceException,
)
from leave.models.leave_balance import LeaveBalance


class LeaveBalanceService:

    @staticmethod
    @transaction.atomic
    def get_balance(employee, leave_type, year):
        return LeaveBalance.objects.select_for_update().get(
            company=employee.company,
            employee=employee,
            leave_type=leave_type,
            year=year,
        )

    @staticmethod
    def get_remaining_days(balance):
        return balance.allocated_days - balance.used_days

    @staticmethod
    @transaction.atomic
    def add_used_days(balance, days):
        balance = LeaveBalance.objects.select_for_update().get(pk=balance.pk)

        days = Decimal(str(days))

        remaining_days = balance.allocated_days - balance.used_days

        if days > remaining_days:
            raise InsufficientLeaveBalanceException()

        balance.used_days += days

        balance.save(update_fields=["used_days", "updated_at"])

        return balance

    @staticmethod
    @transaction.atomic
    def subtract_used_days(balance, days):
        balance = LeaveBalance.objects.select_for_update().get(pk=balance.pk)

        days = Decimal(str(days))

        if days > balance.used_days:
            raise InvalidLeaveBalanceException(
                "Cannot subtract more used leave days than currently used."
            )

        balance.used_days -= days

        balance.save(update_fields=["used_days", "updated_at"])

        return balance
