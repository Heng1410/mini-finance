from django.db import transaction

from employee.models.employee import Employee
from notification.models.notification import Notification


class NotificationService:
    @classmethod
    @transaction.atomic
    def create_notification(cls, *, company, recipient, title, message):
        recipient = Employee.objects.select_for_update().get(
            pk=recipient.pk, company=company
        )

        notification = Notification.objects.create(
            recipient=recipient,
            company=company,
            title=title,
            message=message,
        )

        return notification
