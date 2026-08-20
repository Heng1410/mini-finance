from base.serializers.base_serializer import BaseSerializer
from employee.serializers.employee_serializer import EmployeeSimpleSerializer
from notification.models.notification import Notification


class NotificationSerializer(BaseSerializer):
    recipient = EmployeeSimpleSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ("id", "recipient", "title", "message", "is_read", "read_at")
        read_only_fields = ("id", "recipient", "is_read", "read_at")
