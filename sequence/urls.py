from rest_framework import routers
from django.urls import path, include

from sequence.views.sequence_view_set import SequenceViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"sequences", SequenceViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
