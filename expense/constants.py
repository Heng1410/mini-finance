from django.db import models


class ExpenseStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    APPROVED = "APPROVED", "Approved"
    REJECTED = "REJECTED", "Rejected"
    REIMBURSED = "REIMBURSED", "Reimbursed"
    
class ExpenseCategory(models.TextChoices):
    TRANSPORTATION = "TRANSPORTATION", "Transportation"
    MEALS = "MEALS", "Meals"
    HOTEL = "HOTEL", "Hotel"
    OFFICE = "OFFICE", "Office"
    COMMUNICATION = "COMMUNICATION", "Communication"
    OTHER = "OTHER", "Other"