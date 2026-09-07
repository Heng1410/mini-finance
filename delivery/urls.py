from rest_framework.routers import DefaultRouter
from django.urls import include, path

from delivery.views.delivery_view_set import DeliveryViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"deliveries", DeliveryViewSet)

urlpatterns = [path("", include(router.urls))]
