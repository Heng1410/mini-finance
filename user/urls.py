from django.urls import include,path
from rest_framework import routers

from user.views.user_view_set import UserViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"users", UserViewSet)

urlpatterns = [path("", include(router.urls))]