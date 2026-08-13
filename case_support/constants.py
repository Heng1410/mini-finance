from django.db import models


class CaseStatus(models.TextChoices):
    OPEN = "OPEN", "Open"
    ASSIGNED = "ASSIGNED", "Assigned"
    IN_PROGRESS = "IN_PROGRESS", "In Progress"
    ESCALATED = "ESCALATED", "Escalated"
    RESOLVED = "RESOLVED", "Resolved"
    CLOSED = "CLOSED", "Closed"


class CasePriority(models.TextChoices):
    LOW = "LOW", "Low"
    MEDIUM = "MEDIUM", "Medium"
    HIGH = "HIGH", "High"
    CRITICAL = "CRITICAL", "Critical"


class CaseActivityType(models.TextChoices):
    CREATED = "CREATED", "Created"
    ASSIGNED = "ASSIGNED", "Assigned"
    STATUS_CHANGED = "STATUS_CHANGED", "Status Changed"
    COMMENTED = "COMMENTED", "Commented"
    RESOLVED = "RESOLVED", "Resolved"
    CLOSED = "CLOSED", "Closed"
