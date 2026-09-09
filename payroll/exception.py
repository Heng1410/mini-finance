from rest_framework import status
from rest_framework.exceptions import APIException


class PayrollException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST


class PayrollAlreadyExistsException(PayrollException):
    default_detail = "Payroll already exists for this employee and month."