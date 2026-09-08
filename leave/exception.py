from rest_framework.exceptions import APIException


class LeaveRequestException(APIException):
    status_code = 400
    default_detail = "Invalid leave request operation."
    default_code = "leave_request_error"


class LeaveRequestNotPendingException(LeaveRequestException):
    default_detail = "Only pending leave requests can be rejected."
    default_code = "leave_request_not_pending"
    
class LeaveRequestStatusException(LeaveRequestException):
    default_code = "invalid_leave_request_status"
    

class LeaveBalanceException(APIException):
    status_code = 400
    default_detail = "Invalid leave balance operation."
    default_code = "leave_balance_error"


class InsufficientLeaveBalanceException(LeaveBalanceException):
    default_detail = "Insufficient leave balance."
    default_code = "insufficient_leave_balance"
    
class InvalidLeaveBalanceException(LeaveBalanceException):
    default_detail = "Invalid leave balance operation."
    default_code = "invalid_leave_balance_operation"