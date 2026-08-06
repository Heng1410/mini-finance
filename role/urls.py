from django.urls import include, path
from rest_framework import routers

from role.views.role_view_set import RoleViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"roles", RoleViewSet)

urlpatterns = [path("", include(router.urls))]
