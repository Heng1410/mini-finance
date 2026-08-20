from base.views.company_base_view_set import CompanyBaseViewSet
from notification.models.notification import Notification
from notification.serializers.notification_serializer import NotificationSerializer


class NotificationViewSet(CompanyBaseViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
