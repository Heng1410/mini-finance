from datetime import timedelta

from django.utils import timezone

from employee_document.models.employee_document import EmployeeDocument


class EmployeeDocumentService:

    @staticmethod
    def get_expiring_soon(company, days=30):
        today = timezone.localdate()
        expiry_date = today + timedelta(days=days)

        return EmployeeDocument.objects.select_related(
            "employee",
        ).filter(
            company=company,
            expiry_date__gte=today,
            expiry_date__lte=expiry_date,
        )

    @staticmethod
    def get_expired(company):
        today = timezone.localdate()

        return EmployeeDocument.objects.select_related(
            "employee",
        ).filter(
            company=company,
            expiry_date__lt=today,
        )
        
    @staticmethod
    def delete_document(document):
        if document.file:
            document.file.delete(save=False)
            
        document.delete()
    