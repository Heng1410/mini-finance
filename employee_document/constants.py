from django.db import models


class EmployeeDocumentType(models.TextChoices):
    CONTRACT = "CONTRACT", "Contract"
    ID_DOCUMENT = "ID_DOCUMENT", "ID Document"
    RESUME = "RESUME", "Resume"
    CERTIFICATE = "CERTIFICATE", "Certificate"
    TAX_DOCUMENT = "TAX_DOCUMENT", "Tax Document"
    OTHER = "OTHER", "Other"