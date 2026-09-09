from rest_framework import status
from rest_framework.exceptions import APIException


class ExpenseException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST


class ExpenseNotPendingException(ExpenseException):
    default_detail = "Only pending expenses can be approved or rejected."


class ExpenseNotApprovedException(ExpenseException):
    default_detail = "Only approved expenses can be reimbursed."