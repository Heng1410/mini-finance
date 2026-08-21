from django.urls import include, path
from rest_framework import routers

from travel.views.destination_view_set import DestinationViewSet
from travel.views.travel_expense_view_set import TravelExpenseViewSet
from travel.views.travel_request_approve_view import TravelRequestApproveView
from travel.views.travel_request_complete_view import TravelRequestCompleteView
from travel.views.travel_request_reject_view import TravelRequestRejectView
from travel.views.travel_request_submit_view import TravelRequestSubmitView
from travel.views.travel_request_view_set import TravelRequestViewSet

router = routers.DefaultRouter(trailing_slash=False)

router.register(r"travel/destinations", DestinationViewSet)
router.register(r"travel/travel-request", TravelRequestViewSet)
router.register(r"travel/travel-expense", TravelExpenseViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "travel/travel-request/<int:pk>/submit",
        TravelRequestSubmitView.as_view(),
    ),
    path(
        "travel/travel-request/<int:pk>/approve",
        TravelRequestApproveView.as_view(),
    ),
    path(
        "travel/travel-request/<int:pk>/reject",
        TravelRequestRejectView.as_view(),
    ),
    path(
        "travel/travel-request/<int:pk>/complete",
        TravelRequestCompleteView.as_view(),
    ),
]
