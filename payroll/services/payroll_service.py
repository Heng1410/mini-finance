from django.utils import timezone
from decimal import Decimal

from django.db import IntegrityError, transaction

from payroll.exception import PayrollAlreadyExistsException
from payroll.models.payroll import Payroll


class PayrollService:

    @staticmethod
    @transaction.atomic
    def create_payroll(
        employee,
        year,
        month,
        basic_salary,
        allowance=Decimal("0.00"),
        deduction=Decimal("0.00"),
    ):
        if Payroll.objects.filter(
            company=employee.company,
            employee=employee,
            year=year,
            month=month,
        ).exists():
            raise PayrollAlreadyExistsException()

        net_salary = basic_salary + allowance - deduction

        try:
            return Payroll.objects.create(
                company=employee.company,
                employee=employee,
                year=year,
                month=month,
                basic_salary=basic_salary,
                allowance=allowance,
                deduction=deduction,
                net_salary=net_salary,
            )
        except IntegrityError:
            raise PayrollAlreadyExistsException()


    @staticmethod
    @transaction.atomic
    def mark_paid(payroll):
        payroll.is_paid = True
        payroll.paid_at = timezone.now()

        payroll.save(update_fields=["is_paid", "paid_at", "updated_at"])

        return payroll
