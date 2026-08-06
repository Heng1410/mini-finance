from django.urls import include, path
from rest_framework import routers

from account.views.account_view_set import AccountViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"accounts", AccountViewSet)

urlpatterns = [path("", include(router.urls))]
