from django.db import transaction

from django.utils import timezone

from expense.constants import ExpenseStatus
from expense.exception import ExpenseNotApprovedException, ExpenseNotPendingException
from expense.models.expense import Expense


class ExpenseService:

    @staticmethod
    @transaction.atomic
    def create_expense(employee, date, category, description, amount):
        return Expense.objects.create(
            company=employee.company,
            employee=employee,
            date=date,
            category=category,
            description=description,
            amount=amount,
            status=ExpenseStatus.PENDING,
        )

    @staticmethod
    @transaction.atomic
    def approve(expense):
        if expense.status != ExpenseStatus.PENDING:
            raise ExpenseNotPendingException()

        expense.status = ExpenseStatus.APPROVED
        expense.save(update_fields=["status", "updated_at"])

        return expense

    @staticmethod
    @transaction.atomic
    def reject(expense):
        if expense.status != ExpenseStatus.PENDING:
            raise ExpenseNotPendingException()

        expense.status = ExpenseStatus.REJECTED
        expense.save(update_fields=["status", "updated_at"])

        return expense

    @staticmethod
    @transaction.atomic
    def reimburse(expense):
        if expense.status != ExpenseStatus.APPROVED:
            raise ExpenseNotApprovedException()

        expense.status = ExpenseStatus.REIMBURSED
        expense.reimbursed_at = timezone.now()

        expense.save(update_fields=["status", "reimbursed_at", "updated_at"])

        return expense
