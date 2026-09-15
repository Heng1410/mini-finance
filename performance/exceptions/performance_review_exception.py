from rest_framework import status
from rest_framework.exceptions import APIException


class PerformanceReviewException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST


class PerformanceReviewAlreadySubmittedException(PerformanceReviewException):
    default_detail = "Performance review has already been submitted."


class PerformanceReviewNotSubmittedException(PerformanceReviewException):
    default_detail = "Performance review must be submitted before it can be acknowledged."


class PerformanceReviewAlreadyAcknowledgedException(PerformanceReviewException):
    default_detail = "Performance review has already been acknowledged."