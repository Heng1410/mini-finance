from django.urls import include, path
from rest_framework import routers

from expense.views.expense_view_set import ExpenseViewSet


router = routers.DefaultRouter(trailing_slash=False)
router.register(r"expenses", ExpenseViewSet)

urlpatterns = [path("", include(router.urls))]
