from django.core.exceptions import ValidationError
from django.db import models

from base.models.company_base_model import CompanyBaseModel
from employee.models.employee import Employee
from performance.constants import PerformanceReviewStatus


class PerformanceReview(CompanyBaseModel):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="performance_reviews",
    )
    reviewer = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="reviews_given",
    )
    review_period_start = models.DateField()
    review_period_end = models.DateField()
    rating = models.PositiveSmallIntegerField()
    comments = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=PerformanceReviewStatus.choices,
        default=PerformanceReviewStatus.DRAFT,
    )

    class Meta:
        db_table = "performance_reviews"
        ordering = ["-review_period_end", "-created_at"]

    def clean(self):
        if self.review_period_end < self.review_period_start:
            raise ValidationError(
                {
                    "review_period_end": (
                        "Review period end must be later than or equal to "
                        "review period start."
                    )
                }
            )

        if not 1 <= self.rating <= 5:
            raise ValidationError(
                {
                    "rating": "Rating must be between 1 and 5."
                }
            )