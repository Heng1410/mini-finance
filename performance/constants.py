from django.db import models


class PerformanceReviewStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    SUBMITTED = "SUBMITTED", "Submitted"
    ACKNOWLEDGED = "ACKNOWLEDGED", "Acknowledged"