from django.urls import include,path
from rest_framework import routers

from notification.views.notification_view_set import NotificationViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"notifications", NotificationViewSet)

urlpatterns = [
    path("",include(router.urls))
]