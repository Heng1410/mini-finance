from django.db import transaction

from performance.constants import PerformanceReviewStatus
from performance.models.performance_review import PerformanceReview
from performance.exceptions.performance_review_exception import (
    PerformanceReviewAlreadyAcknowledgedException,
    PerformanceReviewAlreadySubmittedException,
    PerformanceReviewNotSubmittedException,
)


class PerformanceReviewService:

    @staticmethod
    @transaction.atomic
    def create_review(
        employee, reviewer, review_period_start, review_period_end, rating, comments=""
    ):
        return PerformanceReview.objects.create(
            company=employee.company,
            employee=employee,
            reviewer=reviewer,
            review_period_start=review_period_start,
            review_period_end=review_period_end,
            rating=rating,
            comments=comments,
            status=PerformanceReviewStatus.DRAFT,
        )

    @staticmethod
    @transaction.atomic
    def submit(review):
        if review.status != PerformanceReviewStatus.DRAFT:
            raise PerformanceReviewAlreadySubmittedException()

        review.status = PerformanceReviewStatus.SUBMITTED
        review.save(update_fields=["status", "updated_at"])

        return review

    @staticmethod
    @transaction.atomic
    def acknowledge(review):
        if review.status != PerformanceReviewStatus.SUBMITTED:
            if review.status == PerformanceReviewStatus.ACKNOWLEDGED:
                raise PerformanceReviewAlreadyAcknowledgedException()

            raise PerformanceReviewNotSubmittedException()

        review.status = PerformanceReviewStatus.ACKNOWLEDGED
        review.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return review
